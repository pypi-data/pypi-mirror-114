"""
The “out-of-line”, “API mode” gives you the most flexibility and speed to access a C library at the level of C, instead of at the binary level:
"""
# in a separate file "package/foo_build.py"

import cffi


ffibuilder = cffi.FFI()
ffibuilder.set_source(
    module_name="image_intensities._native_code._image_intensities",
    source="""
    #include "definitions.h"
    #include "turbojpeg.h"
    """,
    include_dirs=[  # -I
        "./_native_code/turbojpeg",
        "./_native_code"
    ],
    libraries=[  # -L
        "./_native_code/jpeg",
        "./_native_code/png",
    ],
    sources=[
         "./_native_code/turbojpeg/jsimd_none.c",
         "./_native_code/turbojpeg/jchuff.c",
         "./_native_code/turbojpeg/jcapimin.c",
         "./_native_code/turbojpeg/jcapistd.c",
         "./_native_code/turbojpeg/jccolor.c",
         "./_native_code/turbojpeg/jcicc.c",
         "./_native_code/turbojpeg/jccoefct.c",
         "./_native_code/turbojpeg/jcinit.c",
         "./_native_code/turbojpeg/jcdctmgr.c",
         "./_native_code/turbojpeg/jcmainct.c",
         "./_native_code/turbojpeg/jcmarker.c",
         "./_native_code/turbojpeg/jcmaster.c",
         "./_native_code/turbojpeg/jcomapi.c",
         "./_native_code/turbojpeg/jcparam.c",
         "./_native_code/turbojpeg/jcphuff.c",
         "./_native_code/turbojpeg/jcprepct.c",
         "./_native_code/turbojpeg/jcsample.c",
         "./_native_code/turbojpeg/jctrans.c",
         "./_native_code/turbojpeg/jdapimin.c",
         "./_native_code/turbojpeg/jdapistd.c",
         "./_native_code/turbojpeg/jdatadst.c",
         "./_native_code/turbojpeg/jdatasrc.c",
         "./_native_code/turbojpeg/jdcoefct.c",
         "./_native_code/turbojpeg/jdcolor.c",
         "./_native_code/turbojpeg/jddctmgr.c",
         "./_native_code/turbojpeg/jdhuff.c",
         "./_native_code/turbojpeg/jdicc.c",
         "./_native_code/turbojpeg/jdinput.c",
         "./_native_code/turbojpeg/jdmainct.c",
         "./_native_code/turbojpeg/jdmarker.c",
         "./_native_code/turbojpeg/jdmaster.c",
         "./_native_code/turbojpeg/jdmerge.c",
         "./_native_code/turbojpeg/jdphuff.c",
         "./_native_code/turbojpeg/jdpostct.c",
         "./_native_code/turbojpeg/jdsample.c",
         "./_native_code/turbojpeg/jdtrans.c",
         "./_native_code/turbojpeg/jerror.c",
         "./_native_code/turbojpeg/jfdctflt.c",
         "./_native_code/turbojpeg/jfdctfst.c",
         "./_native_code/turbojpeg/jfdctint.c",
         "./_native_code/turbojpeg/jidctflt.c",
         "./_native_code/turbojpeg/jidctfst.c",
         "./_native_code/turbojpeg/jidctint.c",
         "./_native_code/turbojpeg/jidctred.c",
         "./_native_code/turbojpeg/jquant1.c",
         "./_native_code/turbojpeg/jquant2.c",
         "./_native_code/turbojpeg/jutils.c",
         "./_native_code/turbojpeg/jmemmgr.c",
         "./_native_code/turbojpeg/jmemnobs.c",
         "./_native_code/turbojpeg/jaricom.c",
         "./_native_code/turbojpeg/jdarith.c",
         "./_native_code/turbojpeg/jcarith.c",
         "./_native_code/turbojpeg/turbojpeg.c",
         "./_native_code/turbojpeg/transupp.c",
         "./_native_code/turbojpeg/jdatadst-tj.c",
         "./_native_code/turbojpeg/jdatasrc-tj.c",
         "./_native_code/turbojpeg/rdbmp.c",
         "./_native_code/turbojpeg/rdppm.c",
         "./_native_code/turbojpeg/wrbmp.c",
         "./_native_code/turbojpeg/wrppm.c",

         "./_native_code/intensities.c",
         "./_native_code/png.c",
         "./_native_code/jpeg.c",
     ],
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
