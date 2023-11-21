# -*- mode: python ; coding: utf-8 -*-
from __future__ import annotations
import os
from pathlib import Path
from tempfile import TemporaryDirectory

from PyInstaller.building.utils import get_code_object

from transform_source import transform

import libapp


LIBAPP_ROOT = Path(libapp.__file__).parent
SITE_ROOT = LIBAPP_ROOT.parent

TRANSFORM_DISABLED = ("DISABLE_SOURCE_TRANSFORM" in os.environ)

_TRANSFORMED_OUT = TemporaryDirectory()
TRANSFORMED_OUT = Path(_TRANSFORMED_OUT.name)


def _transform_source_files(an: Analysis) -> list[tuple[str, str, str]]:
    transformed_files = []

    for (name, pth, typecode) in an.pure:
        oldpth = Path(pth)
        if oldpth.is_relative_to(LIBAPP_ROOT):
            new_src = transform(oldpth)
            relpth = oldpth.relative_to(SITE_ROOT)
            newpth = TRANSFORMED_OUT.joinpath(relpth)
            print(f"Writing source for {str(oldpth)!r} to {str(newpth)!r}")
            newpth.parent.mkdir(parents=True, exist_ok=True)
            with open(newpth, "w") as f:
                f.write(new_src)
            transformed_files.append((name, oldpth, newpth))

    return transformed_files


class TransformedSourcePYZ(PYZ):
    def __init__(self, *args, transformed_files: list, **kwargs):
        self._transformed_files = transformed_files
        super().__init__(*args, **kwargs)

    def assemble(self):
        for (name, oldpth, newpth) in self._transformed_files:
            code = get_code_object(name, newpth)
            self.code_dict[name] = code.replace(co_filename=str(oldpth))

        super().assemble()


a = Analysis(
    ['patch.py', 'main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)


if TRANSFORM_DISABLED:
    print("SKIPPING source transformation")
    pyz = PYZ(a.pure)
else:
    transformed_files = _transform_source_files(a)
    pyz = TransformedSourcePYZ(a.pure, transformed_files=transformed_files)


DIST_NAME = "app_broken" if TRANSFORM_DISABLED else "app"


exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=DIST_NAME,
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
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=DIST_NAME,
)
