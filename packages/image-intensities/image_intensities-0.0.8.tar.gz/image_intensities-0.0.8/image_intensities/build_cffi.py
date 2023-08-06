"""
The “out-of-line”, “API mode” gives you the most flexibility and speed to access a C library at the level of C, instead of at the binary level:
"""
# in a separate file "package/foo_build.py"

import cffi
from pathlib import Path

with open(str(Path(__file__).absolute().parent / 'build_cffi.c-files.txt'), 'r') as f:
    sources = f.read().strip().splitlines()
# end with

ffibuilder = cffi.FFI()
ffibuilder.set_source(
    module_name="image_intensities._native_code._image_intensities",
    source="""
    #include "_native_code/definitions.h"
    #include "_native_code/turbojpeg.h"
    """,
    include_dirs=[  # -I
        "./_native_code/turbojpeg",
        "./_native_code"
    ],
    libraries=[  # -L
        "./_native_code/jpeg",
        "./_native_code/png",
    ],
    sources=[f'./_native_code/{filename}' for filename in sources if filename],
    extra_compile_args=[
        "-std=c99",
        "-fPIC",
        "-O3",
        "-DPPM_SUPPORTED",
        "-DBMP_SUPPORTED",
    ],
)
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
