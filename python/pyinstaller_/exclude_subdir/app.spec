# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path

block_cipher = None


# NOTE:__file__ isn't available here, SPEC serves the same role
# https://pyinstaller.readthedocs.io/en/stable/spec-files.html#globals-available-to-the-spec-file
HERE = Path(SPEC).parent.resolve()
EXTRA_DATA_DIR = HERE.joinpath("extra_data")
EXCLUDED_SUBDIR = EXTRA_DATA_DIR.joinpath("excluded_subdir")


datas = []

for pth in EXTRA_DATA_DIR.glob("**/*"):
    p = str(pth)
    if pth == EXCLUDED_SUBDIR or EXCLUDED_SUBDIR in pth.parents:
        print(f"Excluding: {p!r}")
    else:
        dest = str(pth.parent.relative_to(HERE))
        print(f"Including {p!r} in distribution as {dest!r}")
        datas += [(p, dest)]


a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='app',
)
