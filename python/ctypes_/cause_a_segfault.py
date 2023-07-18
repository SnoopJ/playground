import ctypes


def boom():
    """Cause a segmentation fault"""
    ctypes.string_at(0)
