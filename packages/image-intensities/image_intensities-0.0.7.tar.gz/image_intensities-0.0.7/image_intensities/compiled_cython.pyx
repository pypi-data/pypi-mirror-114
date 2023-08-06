#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
convert the image into the yuv colorspace, drop the u and v components,
and then average the y component over 4 evenly-spaced rectangles on the
image dimensions that gives you a floating point number
"""

from typing import Union

from PIL import Image
from luckydonaldUtils.logger import logging
from libc.stdint cimport uint32_t

__author__ = 'luckydonald'


logger = logging.getLogger(__name__)
if __name__ == '__main__':
    logging.add_colored_handler(level=logging.DEBUG)
# end if
logger.debug('loaded Cython version.')

cdef class C_RGB(object):
    cdef int r
    cdef int g
    cdef int b

    def __init__(
        self,
        r: int = 0,
        g: int = 0,
        b: int = 0,
    ):
        self.r = r
        self.g = g
        self.b = b
    # end def

    def __repr__(self):
        return f"{self.__class__.__name__}(r={self.r!r}, g={self.g!r}, b={self.b!r})"
    # end def
# end class


cdef class C_Sums(object):
    cdef C_RGB nw
    cdef C_RGB ne
    cdef C_RGB sw
    cdef C_RGB se

    # noinspection PyShadowingNames
    def __init__(
        self,
        nw: Union[None, C_RGB] = None,
        ne: Union[None, C_RGB] = None,
        sw: Union[None, C_RGB] = None,
        se: Union[None, C_RGB] = None,
    ):
        if nw is None:
            nw = C_RGB()
        # end if
        self.nw = nw
        if ne is None:
            ne = C_RGB()
        # end if
        self.ne = ne
        if sw is None:
            sw = C_RGB()
        # end if
        self.sw = sw
        if se is None:
            se = C_RGB()
        # end if
        self.se = se
    # end def

    def __repr__(self):
        return f"{self.__class__.__name__}(nw={self.nw!r}, ne={self.ne!r}, sw={self.sw!r}, se={self.se!r})"
    # end def
# end class


cdef class C_Luma(object):
    cdef float nw
    cdef float ne
    cdef float sw
    cdef float se

    def __init__(self, nw: float, ne: float, sw: float, se: float):
        self.nw = nw
        self.ne = ne
        self.sw = sw
        self.se = se

    # end def

    def __repr__(self):
        return f"{self.__class__.__name__}(nw={self.nw!r}, ne={self.ne!r}, sw={self.sw!r}, se={self.se!r})"
    # end def
# end class


cpdef C_Sums rgb_sums(img: Image.Image, log_prefix = ""):
    cdef uint32_t width, height, i, j

    width, height = img.size
    pixels = list(img.getdata())
    sums = C_Sums()

    cdef int nw, ne, sw, se, log_counter
    log_counter = -1  # more efficient then i % 10 == 0
    for i in range(height):
        log_counter += 1
        if log_counter == 10:
            logger.debug(f'{log_prefix}Processing line {i} of {width}x{height} px image.')
            log_counter = 0
        # end if
        for j in range(width):
            nw = (i <= height / 2) and (j <= width / 2)
            # noinspection PyShadowingNames
            ne = (i <= height / 2) and (j >= width / 2)
            # noinspection PyShadowingNames
            sw = (i >= height / 2) and (j <= width / 2)
            # noinspection PyShadowingNames
            se = (i >= height / 2) and (j >= width / 2)

            img.load()
            pixel = pixels[i * width + j]
            r, g, b = pixel[0], pixel[1], pixel[2]

            if nw:
                sums.nw.r += r
                sums.nw.g += g
                sums.nw.b += b
            # end if

            if ne:
                sums.ne.r += r
                sums.ne.g += g
                sums.ne.b += b
            # end if

            if sw:
                sums.sw.r += r
                sums.sw.g += g
                sums.sw.b += b
            # end if

            if se:
                sums.se.r += r
                sums.se.g += g
                sums.se.b += b
            # end if
        # end for
    # end for
    return sums
# end def


# noinspection PyShadowingBuiltins
cdef double _calculate_luma(double dim, sum: C_RGB):
    return (
       (sum.r / dim * 0.2126) +
       (sum.g / dim * 0.7152) +
       (sum.b / dim * 0.0772)
    ) / 3.0
# end def


cpdef C_Luma sums_to_luma(sums: C_Sums, img: Image.Image):
    cdef uint32_t width, height
    width, height = img.size

    cdef double dim = max(width * height / 4.0, 1)

    return C_Luma(
        nw=_calculate_luma(dim, sums.nw),
        ne=_calculate_luma(dim, sums.ne),
        sw=_calculate_luma(dim, sums.sw),
        se=_calculate_luma(dim, sums.se),
    )
# end def


def rgb_luma_from_filename(filename: str) -> C_Luma:
    from PIL.Image import open
    img = open(filename)
    result = rgb_sums(img)
    return sums_to_luma(result, img)
# end def
