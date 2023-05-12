# -*- mode: python ; coding: utf-8 -*-
import os
import json
from dataclasses import dataclass

from PyInstaller.utils.hooks import collect_all


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


analysis_cache_fn = os.environ.get("PYI_ANALYSIS_CACHE")
if analysis_cache_fn:
    print(f"Using cached analysis from {analysis_cache_fn!r}")
    a = CachedAnalysis.from_json_file(analysis_cache_fn)
else:
    print("Running main analysis")
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

    with open("analysis_cache.json", "w") as f:
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
