# -*- mode: python ; coding: utf-8 -*-
import os
from pathlib import Path


HERE = Path(SPECPATH).parent
WITH_TESTS = (os.environ.get("WITH_TESTS") is not None)

block_cipher = None


main_a = Analysis(
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

main_pyz = PYZ(main_a.pure, main_a.zipped_data, cipher=block_cipher)

main_exe = EXE(
    main_pyz,
    main_a.scripts,
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

extra_collects = []
if WITH_TESTS:
    test_datas = [str(pth) for pth in Path(HERE, "tests").glob("**/*")]

    run_tests_a = Analysis(
        ['run_tests.py'],
        pathex=[],
        binaries=[],
        datas=test_datas,
        hiddenimports=["main"],
        hookspath=[],
        hooksconfig={},
        runtime_hooks=[],
        excludes=[],
        win_no_prefer_redirects=False,
        win_private_assemblies=False,
        cipher=block_cipher,
        noarchive=False,
    )

    run_tests_pyz = PYZ(run_tests_a.pure, run_tests_a.zipped_data, cipher=block_cipher)

    run_tests_exe = EXE(
        run_tests_pyz,
        run_tests_a.scripts,
        [],
        exclude_binaries=True,
        name='run_tests',
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

    MERGE(
        (main_a, "main", "main"),
        (run_tests_a, "run_tests", "run_tests"),
    )

    extra_collects.extend([
        run_tests_exe,
        run_tests_a.binaries,
        run_tests_a.zipfiles,
        run_tests_a.datas,
    ])

main_coll = COLLECT(
    main_exe,
    main_a.binaries,
    main_a.zipfiles,
    main_a.datas,

    *extra_collects,

    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
