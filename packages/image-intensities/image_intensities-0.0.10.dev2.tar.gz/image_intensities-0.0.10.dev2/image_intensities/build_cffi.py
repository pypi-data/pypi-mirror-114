"""
The “out-of-line”, “API mode” gives you the most flexibility and speed to access a C library at the level of C, instead of at the binary level:
"""
# in a separate file "package/foo_build.py"

import cffi
from pathlib import Path

__folder__ = Path(__file__).absolute().parent
with open(__folder__.joinpath('build_cffi.c-files.txt').as_posix(), 'r') as f:
    sources = f.read().strip().splitlines()
# end with

ext_dir = __folder__.joinpath('_image_intensities')
sources = [ext_dir.joinpath(s).as_posix() for s in sources if s]

ffibuilder = cffi.FFI()
args = dict(
    module_name="image_intensities._native_code._image_intensities",
    source="""
    #include "definitions.h"
    #include "turbojpeg.h"
    """,
    include_dirs=[  # -I
        ext_dir.joinpath("./_native_code/turbojpeg").as_posix(),
        ext_dir.joinpath("./_native_code").as_posix(),
    ],
    libraries=[  # -L
        ext_dir.joinpath("./_native_code/jpeg").as_posix(),
        ext_dir.joinpath("./_native_code/png").as_posix(),
    ],
    sources=sources,
    extra_compile_args=[
        "-std=c99",
        "-fPIC",
        "-O3",
        "-DPPM_SUPPORTED",
        "-DBMP_SUPPORTED",
    ],

)

print('ffibuilder args')
print(args)

ffibuilder.set_source(**args)
ffibuilder.cdef("""
    struct intensity_data {
        double nw;
        double ne;
        double sw;
        double se;
        int error;
    };

    struct intensity_data jpeg_intensities(const char *file_name);
    struct intensity_data png_intensities(const char *file_name);
""")

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
# end if
