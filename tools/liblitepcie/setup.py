from distutils.core import setup, Extension

extension_mod = Extension("_liblitepcie", ["liblitepcie.cc", "../../build/acorn_cle_215/driver/user/liblitepcie.c"],
                          include_dirs=["../../build/acorn_cle_215/driver/user/", "../../build/acorn_cle_215/driver/kernel/"])

setup(name = "liblitepcie", ext_modules=[extension_mod])
