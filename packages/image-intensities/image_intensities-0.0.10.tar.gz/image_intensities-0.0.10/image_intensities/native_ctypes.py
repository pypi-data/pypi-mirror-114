#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from luckydonaldUtils.logger import logging

__author__ = 'luckydonald'

logger = logging.getLogger(__name__)
if __name__ == '__main__':
    logging.add_colored_handler(level=logging.DEBUG)
# end if


import ctypes
import pathlib
from luckydonaldUtils.encoding import to_binary as b

from .pure_python import Luma
from .shared_cffi import lib_jpeg_intensities, lib_png_intensities, lib_rgb_luma_from_filename

# Load the shared library into ctypes
libname = pathlib.Path().absolute() / "_native_code" / "lib" / "libimage_intensities.so"
if not libname.exists():
    raise ImportError(f'Could not find library at {libname!s}.')
# end if


libname = str(libname)
logger.debug(f'Image intensities library path: {libname!r}')

c_lib = ctypes.CDLL(libname)


class IntensityData(ctypes.Structure):
    _fields_ = [
        ("nw", ctypes.c_double),
        ("ne", ctypes.c_double),
        ("sw", ctypes.c_double),
        ("se", ctypes.c_double),
    ]
# end class


c_lib.jpeg_intensities.restype = IntensityData
c_lib.png_intensities.restype = IntensityData

# struct intensity_data jpeg_intensities(const char *file_name);
# struct intensity_data png_intensities(const char *file_name);


def jpeg_intensities(file_name: str) -> Luma:
    return lib_jpeg_intensities(ctypes.c_char_p(b(file_name)), c_lib)
# end def


def png_intensities(file_name: str) -> Luma:
    return lib_png_intensities(ctypes.c_char_p(b(file_name)), c_lib)
# end def


def rgb_luma_from_filename(file_name: str) -> Luma:
    return lib_rgb_luma_from_filename(file_name, ctypes.c_char_p(b(file_name)), c_lib)
# end def
