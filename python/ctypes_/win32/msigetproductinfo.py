import ctypes
from ctypes.wintypes import DWORD
from ctypes import c_char_p, POINTER, c_uint


LPDWORD = POINTER(DWORD)

MsiGetProductInfo = ctypes.windll.msi.MsiGetProductInfoA
MsiGetProductInfo.argtypes = (c_char_p, c_char_p, c_char_p, LPDWORD)
MsiGetProductInfo.restype = c_uint


def install_location(guid: bytes):
    """
    Retrieves the InstallLocation property of the Windows Installer product with the given GUID

    For more information, see the Win32 API documentation:
    https://docs.microsoft.com/en-us/windows/win32/api/msi/nf-msi-msigetproductinfoa

    Parameters
    ----------
    guid: bytes
        Product GUID in MS format, i.e. `b"{xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx}"`
    """
    # NOTE: output buffer large enough for an extended path (plus null terminator)
    OUTSZ = 2**15
    outbuf = ctypes.create_string_buffer(OUTSZ)

    result = MsiGetProductInfo(guid, b"InstallLocation", outbuf, ctypes.byref(DWORD(OUTSZ)))

    if result != 0:
        raise RuntimeError(f"Unable to retrieve product InstallLocation") from ctypes.WinError(result)

    return outbuf.value.decode()
