# -*- mode: python ; coding: utf-8 -*-
import os
import os.path
import json
import shutil
from dataclasses import dataclass
from pathlib import Path

from PyInstaller.log import logger as LOGGER
from PyInstaller.utils.hooks import collect_all


WORKDIR = Path(workpath)
HERE = Path(SPECPATH)
CACHE_DIR = HERE.joinpath("pyi_analysis_cache")
CACHE_DIR.mkdir(exist_ok=True)
ANALYSIS_CACHE = CACHE_DIR.joinpath("analysis_cache.json")
BASE_LIB_BUILT = WORKDIR.joinpath("base_library.zip")
BASE_LIB_CACHE = CACHE_DIR.joinpath("base_library.zip")

block_cipher = None

@dataclass
class CachedAnalysis:
    scripts: TOC
    pure: TOC
    binaries: TOC
    datas: TOC
    zipfiles: TOC

    @classmethod
    def from_json_file(cls, fn):
        with open(fn, "r") as f:
            cached = json.load(f)

            args = {}
            for k in ("scripts", "pure", "binaries", "datas", "zipfiles"):
                contents = [tuple(entry) for entry in cached[k]]
                args[k] = TOC(contents)

        return cls(**args)


use_cache = os.environ.get("PYI_ANALYSIS_CACHE")
if use_cache:
    LOGGER.info(f"Using cached analysis from {str(CACHE_DIR)!r}")
    a = CachedAnalysis.from_json_file(ANALYSIS_CACHE)
    if BASE_LIB_CACHE.exists():
        shutil.copy(BASE_LIB_CACHE, WORKDIR)
else:
    LOGGER.info("Running main analysis")
    a = Analysis(
        ['main.py'],
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

    with open(ANALYSIS_CACHE, "w") as f:
        json.dump({
                "scripts": list(a.scripts),
                "pure": list(a.pure),
                "binaries": list(a.binaries),
                "datas": list(a.datas),
                "zipfiles": list(a.zipfiles),
            },
            f,
            indent=4,
        )
        LOGGER.info(f"Analysis cache written to {str(ANALYSIS_CACHE)!r}")

    if BASE_LIB_BUILT.exists():
        shutil.copy(BASE_LIB_BUILT, BASE_LIB_CACHE)
        LOGGER.info(f"base_library.zip cached to {str(BASE_LIB_CACHE)!r}")


pyz = PYZ(a.pure, a.zipfiles, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
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
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
