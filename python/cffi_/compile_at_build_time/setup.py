from setuptools import setup

setup(
    cffi_modules=["src/cffiwhat/_ffi.py:ffi"],
)
