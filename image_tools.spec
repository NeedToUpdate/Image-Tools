# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['image_tools.py'],
    pathex=['C:\\Users\\1337\\Documents\\Programming\\Python\\image_tools\\.venv\\Lib\\site-packages'],
    binaries=[],
    datas=[('C:\\Users\\1337\\Documents\\Programming\\Python\\image_tools\\.venv\\lib\\site-packages\\eel\\eel.js', 'eel'), ('web', 'web')],
    hiddenimports=['bottle_websocket'],
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='image_tools',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)