import ctypes
from ctypes import wintypes as w
from pathlib import Path

from tempfile import TemporaryDirectory

kernel32 = ctypes.windll.kernel32

kernel32.GetVolumeInformationA.argtypes = w.LPCSTR, w.LPSTR, w.DWORD, w.LPDWORD, w.LPDWORD, w.LPDWORD, w.LPSTR, w.DWORD
kernel32.GetVolumeInformationA.restype = w.BOOL

def component_length(volume_root: str) -> int:
    comp_len = w.DWORD()
    kernel32.GetVolumeInformationA(volume_root.encode("utf-8"), None, 0, None, ctypes.pointer(comp_len), None, None, 0)

    return comp_len.value

# On my Win10 system with Long Paths enabled, this outputs:
# For volume root 'C:\\' the maximum component length is 255
# Attempting to create a file with maximum component length filename (255)
#         SUCCESS                                                                                                                                                                 file created: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
# aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
# Attempting to create a file with filename longer than maximum component length (256)
#         FAIL

if __name__ == "__main__":
    with TemporaryDirectory() as tmpdir:
        root = Path(tmpdir).parts[0]
        maxlen = component_length(root)
        print(f"For volume root {root!r} the maximum component length is {maxlen}")

        print(f"Attempting to create a file with maximum component length filename ({maxlen})")
        try:
            fn = "a" * maxlen
            Path(tmpdir, fn).write_text("hello")
            print("\tSUCCESS")
            print(f"\tfile created: {fn}")
        except Exception:
            print("\tFAIL")

        overlen = maxlen + 1
        print(f"Attempting to create a file with filename longer than maximum component length ({overlen})")
        try:
            fn = "b" * overlen
            Path(tmpdir, overlen).write_text("hello again")
            print("\tSUCCESS")
            print("\tfile created: {fn}")
        except Exception:
            print("\tFAIL")
