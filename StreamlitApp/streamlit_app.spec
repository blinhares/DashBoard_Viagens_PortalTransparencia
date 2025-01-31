# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import copy_metadata

datas = [
    # We need to include the streamlit_app.py file and the streamlit package
    ("main.py", "."),
    # assuming, your virtual environment is in the .venv directory
    ("/home/bruno/Documentos/Python/Streamlit_app_exe_padrao/.venv/lib/python3.10/site-packages/streamlit/runtime", "./streamlit/runtime")
    ]
datas += collect_data_files("streamlit")
datas += copy_metadata("streamlit")

block_cipher = None

a = Analysis(
    # The path to the main script
    ['run.py'],
    # https://pyinstaller.org/en/stable/man/pyi-makespec.html?highlight=pathex#what-to-bundle-where-to-search
    pathex=["."],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    # include the custom hooks
    hookspath=['./hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    # The name of the executable file
    name='MeuStreamlitApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
