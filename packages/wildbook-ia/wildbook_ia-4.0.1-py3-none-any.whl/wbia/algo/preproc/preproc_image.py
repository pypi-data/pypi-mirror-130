# -*- coding: utf-8 -*-
import logging
import os
from os.path import splitext, basename, isabs
import warnings
import vtool.exif as vtexif
import utool as ut
from vtool.exif import ORIENTATION_DICT_INVERSE, ORIENTATION_UNDEFINED, ORIENTATION_000
from wbia.utils import call_houston


EXIF_UNDEFINED = ORIENTATION_DICT_INVERSE[ORIENTATION_UNDEFINED]
EXIF_NORMAL = ORIENTATION_DICT_INVERSE[ORIENTATION_000]


(print, rrr, profile) = ut.inject2(__name__)
logger = logging.getLogger('wbia')


def parse_exif(pil_img):
    """Image EXIF helper"""
    exif_dict = vtexif.get_exif_dict(pil_img)
    # TODO: More tags
    # (mainly the orientation tag)
    lat, lon = vtexif.get_lat_lon(exif_dict)
    orient = vtexif.get_orientation(exif_dict, on_error='warn')
    time = vtexif.get_unixtime(exif_dict)
    return time, lat, lon, orient


def get_standard_ext(gpath):
    """Returns standardized image extension"""
    ext = splitext(gpath)[1].lower()
    return '.jpg' if ext == '.jpeg' else ext


@profile
def parse_imageinfo(gpath):
    """Worker function: gpath must be in UNIX-PATH format!

    Args:
        gpath (str): image path

    Returns:
        tuple: param_tup -
            if successful returns a tuple of image parameters which are values
            for SQL columns on else returns None

    CommandLine:
        python -m wbia.algo.preproc.preproc_image --exec-parse_imageinfo

    Doctest:
        >>> from wbia.algo.preproc.preproc_image import *  # NOQA
        >>> gpath = ut.grab_test_imgpath('patsy.jpg')
        >>> param_tup = parse_imageinfo(gpath)
        >>> result = ('param_tup = %s' % (str(param_tup),))
        >>> print(result)
        >>> uuid = param_tup[0]
        >>> assert str(uuid) == '16008058-788c-2d48-cd50-f6029f726cbf'
    """
    # Try to open the image
    from PIL import Image
    import tempfile
    import requests
    import cv2

    import urllib

    urlsplit = urllib.parse.urlsplit
    urlquote = urllib.parse.quote
    urlunquote = urllib.parse.unquote

    gpath = gpath.strip()

    url_protos = ['https://', 'http://']
    s3_proto = ['s3://']
    houston_proto = ['houston+']
    valid_protos = s3_proto + url_protos + houston_proto

    def isproto(gpath, valid_protos):
        return any(gpath.startswith(proto) for proto in valid_protos)

    def islocal(gpath):
        return not (isabs(gpath) and isproto(gpath, valid_protos))

    with warnings.catch_warnings(record=True) as w:
        try:
            if isproto(gpath, valid_protos):
                # suffix = '.%s' % (basename(gpath), )
                filename = basename(gpath)
                _, ext = splitext(filename)
                # base = filename
                base = ut.random_nonce(16)
                suffix = '.%s%s' % (base, ext)
                temp_file, temp_filepath = tempfile.mkstemp(suffix=suffix)
                args = (
                    gpath,
                    temp_filepath,
                )
                logger.info(
                    '[preproc] Caching remote %s file to temporary file %r' % args
                )

                if isproto(gpath, s3_proto):
                    s3_dict = ut.s3_str_decode_to_dict(gpath)
                    ut.grab_s3_contents(temp_filepath, **s3_dict)
                if isproto(gpath, url_protos):
                    # Ensure that the Unicode string is properly encoded for web requests
                    uri_ = urlunquote(gpath)
                    uri_ = urlsplit(uri_, allow_fragments=False)
                    uri_path = urlquote(uri_.path.encode('utf8'))
                    uri_ = uri_._replace(path=uri_path)
                    uri_ = uri_.geturl()
                    try:
                        response = requests.get(uri_, stream=True, allow_redirects=True)
                        assert (
                            response.status_code == 200
                        ), '200 code not received on download'
                    except Exception:
                        parts = urlsplit(uri_, allow_fragments=False)
                        uri_ = uri_[len('%s://' % (parts.scheme,)) :]
                        hostname = urlquote(parts.hostname.encode('utf8'))
                        if parts.port:
                            hostname = f'{hostname}:{parts.port}'
                        uri_ = '%s://%s%s' % (parts.scheme, hostname, parts.path)
                        response = requests.get(uri_, stream=True, allow_redirects=True)
                        assert (
                            response.status_code == 200
                        ), '200 code not received on download'

                    # Save
                    with open(temp_filepath, 'wb') as temp_file_:
                        for chunk in response.iter_content(1024):
                            temp_file_.write(chunk)
                elif isproto(gpath, houston_proto):
                    response = call_houston(gpath)
                    assert (
                        response.status_code == 200
                    ), f'200 code not received on download: {gpath}'
                    with open(temp_filepath, 'wb') as temp_file_:
                        for chunk in response.iter_content(1024):
                            temp_file_.write(chunk)
                gpath_ = temp_filepath
            else:
                temp_file, temp_filepath = None, None
                gpath_ = gpath
        except (
            AssertionError,
            IOError,
            requests.HTTPError,
            urllib.error.HTTPError,
            Image.DecompressionBombError,
        ) as ex:
            # ut.embed()
            logger.info('[preproc] IOError: %s' % (str(ex),))
            return None

        if len(w) > 0:
            # for warn in w:
            #     warnings.showwarning(warn.message, warn.category,
            #                          warn.filename, warn.lineno, warn.file,
            #                          warn.line)
            #     warnstr = warnings.formatwarning
            #     logger.info(warnstr)
            logger.info('%d warnings issued by %r' % (len(w), gpath))

    try:
        # Open image with EXIF support to get time, GPS, and the original orientation
        pil_img = Image.open(gpath_, 'r')

        # Convert 16-bit RGBA images on disk to 8-bit RGB
        if pil_img.mode == 'RGBA':
            pil_img.load()
            canvas = Image.new('RGB', pil_img.size, (255, 255, 255))
            canvas.paste(pil_img, mask=pil_img.split()[3])  # 3 is the alpha channel
            canvas.save(gpath_)
            pil_img = Image.open(gpath_, 'r')

        time, lat, lon, orient = parse_exif(pil_img)  # Read exif tags
        pil_img.close()

        # OpenCV >= 3.1 supports EXIF tags, which will load correctly
        img = cv2.imread(gpath_)
        assert img is not None

        if orient not in [EXIF_UNDEFINED, EXIF_NORMAL]:
            try:
                # Sanitize weird behavior and standardize EXIF orientation to 1
                cv2.imwrite(gpath_, img)
                orient = EXIF_NORMAL
            except AssertionError:
                return None
    except (FileNotFoundError):
        return None

    # Parse out the data
    height, width = img.shape[:2]  # Read width, height

    # We cannot use pixel data as libjpeg is not deterministic (even for reads!)
    image_uuid = ut.get_file_uuid(gpath_)  # Read file ]-hash-> guid = gid

    # orig_gpath = gpath
    orig_gname = basename(gpath)
    ext = get_standard_ext(gpath)
    notes = ''
    # Build parameters tuple
    param_tup = (
        image_uuid,
        gpath,
        gpath,
        orig_gname,
        # orig_gpath,
        ext,
        width,
        height,
        time,
        lat,
        lon,
        orient,
        notes,
    )

    if temp_filepath is not None:
        os.close(temp_file)
        os.unlink(temp_filepath)
    # logger.info('[ginfo] %r %r' % (image_uuid, orig_gname))
    return param_tup


# def add_images_params_gen(gpath_list):
#     """
#     generates values for add_images sqlcommands asychronously

#     Args:
#         gpath_list (list):

#     Kwargs:
#         ordered, force_serial, chunksize, prog, verbose, quiet, nTasks, freq,
#         adjust

#     Returns:
#         generator: params_gen

#     CommandLine:
#         python -m wbia.algo.preproc.preproc_image --exec-add_images_params_gen

#     Example0:
#         >>> # ENABLE_DOCTEST
#         >>> from wbia.algo.preproc.preproc_image import *   # NOQA
#         >>> from vtool.tests import grabdata
#         >>> gpath_list = grabdata.get_test_gpaths(ndata=3) + ['doesnotexist.jpg']
#         >>> params_list = list(add_images_params_gen(gpath_list))
#         >>> assert str(params_list[0][0]) == '66ec193a-1619-b3b6-216d-1784b4833b61', 'UUID gen method changed'
#         >>> assert str(params_list[0][3]) == 'easy1.JPG', 'orig name is different'
#         >>> assert params_list[3] is None
#     """
#     params_gen = ut.generate2(parse_imageinfo, zip(gpath_list), adjust=True,
#                               force_serial=True)
#     return params_gen


def on_delete(ibs, featweight_rowid_list, qreq_=None):
    logger.info('Warning: Not Implemented')
