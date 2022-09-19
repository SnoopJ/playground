"""
This sample shows off some Win32 API usage for adjusting the security settings
of a target directory and files beneath it, to allow writes by everyone.

The original context that caused me to create this sample was wanting to make
a log file located in %PROGRAMDATA% writeable by all Windows users
"""
from pathlib import Path

import win32security, ntsecuritycon


Path("testdir").mkdir(exist_ok=True)
Path("testdir", "testfile").touch()
Path("testdir", "testfile2").touch()

FILENAME = str(Path("testdir").resolve())
EVERYONE_SID = win32security.GetBinarySid("S-1-1-0")

# NOTE: what I tried first, does not work when FILENAME is a directory, possibly
# because SetFileSecurity() is obsolete
#
# sd = win32security.GetFileSecurity(FILENAME, win32security.DACL_SECURITY_INFORMATION)
# dacl = sd.GetSecurityDescriptorDacl()
# dacl.AddAccessAllowedAce(win32security.ACL_REVISION, ntsecuritycon.FILE_ALL_ACCESS, EVERYONE_SID)
# sd.SetSecurityDescriptorDacl(1, dacl, 0)
# win32security.SetFileSecurity(FILENAME, win32security.DACL_SECURITY_INFORMATION, sd)


# adapted from https://stackoverflow.com/a/43244697
entries = [
    {
        'AccessMode': win32security.GRANT_ACCESS,
        'AccessPermissions': ntsecuritycon.FILE_ALL_ACCESS,
        'Inheritance': win32security.CONTAINER_INHERIT_ACE | win32security.OBJECT_INHERIT_ACE,
        'Trustee': {
            'TrusteeType': win32security.TRUSTEE_IS_USER,
            'TrusteeForm': win32security.TRUSTEE_IS_SID,
            'Identifier': EVERYONE_SID}
    }
]

sd = win32security.GetNamedSecurityInfo(
    FILENAME,
    win32security.SE_FILE_OBJECT,
    win32security.DACL_SECURITY_INFORMATION
)
dacl = sd.GetSecurityDescriptorDacl()
dacl.SetEntriesInAcl(entries)
win32security.SetNamedSecurityInfo(
    FILENAME,
    win32security.SE_FILE_OBJECT,
    win32security.DACL_SECURITY_INFORMATION | win32security.UNPROTECTED_DACL_SECURITY_INFORMATION,
    None,
    None,
    dacl,
    None
)
