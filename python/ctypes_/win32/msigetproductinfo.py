import ctypes
from ctypes.wintypes import DWORD
from ctypes import c_char_p, POINTER, c_uint
import typing as t
 
LPDWORD = POINTER(DWORD)
 
MsiEnumRelatedProducts = ctypes.windll.msi.MsiEnumRelatedProductsA
MsiEnumRelatedProducts.argtypes = (c_char_p, DWORD, DWORD, c_char_p)
MsiEnumRelatedProducts.restype = c_uint

MsiGetProductInfo = ctypes.windll.msi.MsiGetProductInfoA
MsiGetProductInfo.argtypes = (c_char_p, c_char_p, c_char_p, LPDWORD)
MsiGetProductInfo.restype = c_uint

# NOTE:Selected Win32 API error codes https://docs.microsoft.com/en-us/windows/win32/debug/system-error-codes--0-499-
ERROR_SUCCESS = 0
ERROR_NO_MORE_ITEMS = 0x103


def enumerate_products(upgradecode: bytes) -> t.List[bytes]:
    """
    Enumerates products with the given UpgradeCode GUID

    For more information, see the Win32 API documentation:
    https://docs.microsoft.com/en-us/windows/win32/api/msi/nf-msi-msienumrelatedproductsa

    Parameters
    ----------
    upgradecode: bytes
        UpgradeCode GUID in MS format, i.e. `b"{xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx}"`

    Notes
    -----
    The UpgradeCode will be consistent between versions of a particular package, and
    the ProductCode will change with each version.
    """
    # NOTE: output buffer large enough for a GUID
    OUTSZ = 64
    outbuf = ctypes.create_string_buffer(OUTSZ)

    results = []

    idx = 0
    while True:
        err = MsiEnumRelatedProducts(upgradecode, 0, idx, outbuf)
        idx += 1
        if err == ERROR_SUCCESS:
            results.append(outbuf.value)
        elif err == ERROR_NO_MORE_ITEMS:
            break
        else:
            raise RuntimeError(f"Error while enumerating products with UpgradeCode {upgradecode}") from ctypes.WinError(err)

    return results


def install_location(productcode: bytes) -> str:
    """
    Retrieves the InstallLocation property of the Windows Installer product with the given ProductCode GUID

    For more information, see the Win32 API documentation:
    https://docs.microsoft.com/en-us/windows/win32/api/msi/nf-msi-msigetproductinfoa

    Parameters
    ----------
    productcode: bytes
        ProductCode GUID in MS format, i.e. `b"{xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx}"`
    """
    # NOTE: output buffer large enough for an extended path (plus null terminator)
    OUTSZ = 2**15
    outbuf = ctypes.create_string_buffer(OUTSZ)

    err = MsiGetProductInfo(productcode, b"InstallLocation", outbuf, ctypes.byref(DWORD(OUTSZ)))

    if err != 0:
        raise RuntimeError(f"Unable to retrieve product InstallLocation for ProductCode {productcode}") from ctypes.WinError(err)

    return outbuf.value.decode()

