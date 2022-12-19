# -*- mode: python ; coding: utf-8 -*-
import logging


logger = logging.getLogger(__name__)


block_cipher = None


a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[],
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

def munge_bin(toc_entry):
    oldpath, path, type = toc_entry
    prefix = "lib/"
    if "libpython" not in oldpath:
        newpath = prefix + oldpath
        logger.info("Modifying path %r to %r", oldpath, newpath)
    else:
        # do NOT modify libpython layout, which is enough to get
        # an interpreter that starts up, although it fails during init
        # of the runtime hooks
        newpath = oldpath

    return (newpath, path, type)

oldbins = a.binaries
a.binaries = [munge_bin(entry) for entry in oldbins]

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

