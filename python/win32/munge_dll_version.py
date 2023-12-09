"""
This is a small proof-of-concept program I wrote to see how I could change the
"File Version" of a Windows file.

With thanks to StackOverflow user 0xC0000022L for their helpful answer to a related question:
https://stackoverflow.com/a/17579067

If you're wondering why a program like this might need to exist, this field is
part of how the Windows Installer system decides whether or not a file needs to
be installed when performing a product upgrade. If you are unlucky enough to have
a newer version of your product with files that have a LOWER file version, the
Installer will probably not install that file from your "new" version, and will
remove the file when it gets rid of the "old" version, and now you have a headache. [1]

In particular, this can happen REALLY easily if your installer contains an
application built with PyInstaller, but your PyInstaller distributions were
generated with different builds of the same major Python release. This is almost
never what you want, but that's okay, the Windows Installer helps even if you
don't want it to.

The most expedient fix I found to this problem was to define the REINSTALLMODE
property [2] in my "new" install to mode 'amus', where 'a' means "reinstall all."
But this 'fix' is frowned on in the Windows Installer world because it can be
very unreliable if you have side-by-side installations of different versions of
the same product. *I* don't, but I was annoyed enough by the lack of actual
not-frowned-on solutions to the problem that I decided to indulge myself in some
spite-driven development.


[1] https://learn.microsoft.com/en-us/archive/blogs/astebner/why-windows-installer-removes-files-during-a-major-upgrade-if-they-go-backwards-in-version-numbers
[2] https://learn.microsoft.com/en-us/windows/win32/msi/reinstallmode

"""
from pathlib import Path

import pefile


HERE = Path(__file__).parent.resolve()
TARGET_FILE = HERE.joinpath("python38.dll")


def to_human_ver(ms: int, ls: int):
    """Given the most/least significant version fields, return a human readable version X.Y.Z.W"""
    return (
        ms >> 16,
        ms & 0xFFFF,
        ls >> 16,
        ls & 0xFFFF
    )


def to_inhuman_ver(a: int, b: int, c: int, d: int):
    """Given human readable version X.Y.Z.W, return the most/least significant version fields"""
    # TODO: what if b,d are too large? round-trips fine as is assuming we asked for something that fits the field
    ms = (a << 16) + b
    ls = (c << 16) + d

    return ms, ls


def main():
    dll = pefile.PE(TARGET_FILE)

    assert hasattr(dll, "VS_FIXEDFILEINFO"), f"No file version info present in {TARGET_FILE}"

    verinfo = dll.VS_FIXEDFILEINFO[0]
    filever = to_human_ver(verinfo.FileVersionMS, verinfo.FileVersionLS)
    prodver = to_human_ver(verinfo.ProductVersionMS, verinfo.ProductVersionLS)

    print(f"Properties of {TARGET_FILE}")
    print(f"File version: {filever}")
    print(f"Product version: {prodver}")

    print("Changing file version to 4.0.0.0")
    new_filever_MS, new_filever_LS = to_inhuman_ver(4, 0, 0, 0)

    verinfo.FileVersionMS = new_filever_MS
    verinfo.FileVersionLS = new_filever_LS

    # I tried changing the product name as well, but the changes don't seem to apply. Not sure what I missed,
    # but that's okay, it's not important to my use-case anyway

    #print("Changing product version to 3.1.4.1")
    #new_prodver_MS, new_prodver_LS = to_inhuman_ver(3, 1, 4, 1)

    #verinfo.ProductVersionMS = new_prodver_MS
    #verinfo.ProductVersionLS = new_prodver_LS

    newfile = TARGET_FILE.with_name(TARGET_FILE.stem + ".new" + TARGET_FILE.suffix)
    print(f"Writing file with new file version to {newfile}")
    dll.write(newfile)


if __name__ == "__main__":
    main()

