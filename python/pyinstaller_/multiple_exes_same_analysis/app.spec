# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path


HERE = Path(SPECPATH)
MAIN_PY = HERE.joinpath("main.py")
OTHER_PY = HERE.joinpath("other.py")

ALL_ENTRYPOINTS = [str(MAIN_PY), str(OTHER_PY)]


block_cipher = None

# -----
# Here, we perform a common analysis, effectively getting the union of the
# direct dependencies of each entrypoint. This Analysis produces a `.scripts`
# TOC that WILL NOT produce a meaningful EXE if used directly, because it is
# nonsense to concatenate main.py and other.py, so we will have to post-process
# the Analysis to pull those scripts apart before making our EXEs.
# -----
common_a = Analysis(
    ALL_ENTRYPOINTS,
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

idx = next(idx for idx, (name, pth, toctype) in enumerate(common_a.scripts) if Path(pth) == MAIN_PY)

# The header contains runtime hooks for *all* dependencies
SCRIPTS_HEADER = common_a.scripts[:idx]
# Here, we're hard-coding how many scripts there are and what order they're in. This would need
# to be more careful in a more sophisticated bundle where each entrypoint may be built from multiple scripts
MAIN_SCRIPTS = common_a.scripts[idx:idx + 1]
OTHER_SCRIPTS = common_a.scripts[idx + 1:idx + 2]

# This PYZ will be inserted into both EXEs, which does duplicate some data from the dependencies, but
# as long as the majority of the dependency data is *not* in the PYZ, this duplication should be fine
common_pyz = PYZ(common_a.pure, common_a.zipped_data, cipher=block_cipher)

# Here 
main_exe = EXE(
    common_pyz,
    SCRIPTS_HEADER,
    MAIN_SCRIPTS,
    [],
    exclude_binaries=True,
    name='main',
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


other_exe = EXE(
    common_pyz,
    SCRIPTS_HEADER,
    OTHER_SCRIPTS,
    [],
    exclude_binaries=True,
    name='other',
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
    main_exe,
    other_exe,

    common_a.binaries,
    common_a.zipfiles,
    common_a.datas,

    strip=False,
    upx=True,
    upx_exclude=[],
    name='app',
)
