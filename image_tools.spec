# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['image_tools.py'],
    pathex=['C:\\Users\\1337\\Documents\\Programming\\Python\\image_tools\\.venv\\Lib\\site-packages'],
    binaries=[],
    datas=[('C:\\Users\\1337\\Documents\\Programming\\Python\\image_tools\\.venv\\lib\\site-packages\\eel\\eel.js', 'eel'), ('web', 'web'), ('C:\\Users\\1337\\Documents\\Programming\\Python\\image_tools\\pretrained\\modnet_photographic_portrait_matting.ckpt', 'pretrained')],
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

to_rem = [ 'torch._C', 'torch._C_flatbuffer']

for val in to_rem:
    for b in a.binaries:
          nb = b[0]
          if val in str(nb):
                print("removed  " + b[0])
                a.binaries.remove(b)

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
