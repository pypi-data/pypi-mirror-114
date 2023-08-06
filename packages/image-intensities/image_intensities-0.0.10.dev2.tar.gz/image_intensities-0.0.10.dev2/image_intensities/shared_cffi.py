from mimetypes import guess_type
from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    import cffi
    import ctypes
# end if

from .pure_python import Luma


def convert_struct_to_luma(struct) -> Luma:
    return Luma(nw=struct.nw, ne=struct.ne, sw=struct.sw, se=struct.se)
# end def


def lib_jpeg_intensities(filename, lib: Union['cffi.FFI', 'ctypes.CDLL']) -> Luma:
    # noinspection PyUnresolvedReferences
    return convert_struct_to_luma(lib.jpeg_intensities(filename))
# end def


def lib_png_intensities(filename, lib: Union['cffi.FFI', 'ctypes.CDLL']) -> Luma:
    # noinspection PyUnresolvedReferences
    return convert_struct_to_luma(lib.png_intensities(filename))
# end def


def lib_rgb_luma_from_filename(filename: str, argument_filename, lib):
    (mime_type, encoding) = guess_type(filename)
    if mime_type == 'image/png':
        return lib_png_intensities(argument_filename, lib)
    elif mime_type == 'image/jpeg':
        return lib_jpeg_intensities(argument_filename, lib)
    else:
        raise ValueError('Unknown mime.')
    # end if
# end def
