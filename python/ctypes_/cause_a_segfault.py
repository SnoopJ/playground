import ctypes


def boom():
    """Cause a segmentation fault"""
    ctypes.string_at(0)


if __name__ == "__main__":
    boom()
