from distutils.core import setup, Extension

extension_mod = Extension("_liblitepcie", ["liblitepcie.c", "../../build/acorn_cle_215/driver/user/liblitepcie.c"],
                          include_dirs=["../../build/acorn_cle_215/driver/user/", "../../build/acorn_cle_215/driver/kernel/"],
                          language="c")

setup(name = "liblitepcie", ext_modules=[extension_mod])
