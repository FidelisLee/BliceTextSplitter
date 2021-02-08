block_cipher = None
a = Analysis(['ToolBoxWindow.py'],
    pathex=['D:\\Python\\workspace_python\\ToolBox'],
    binaries=None,
    datas=None,
    hiddenimports=[],
    hookspath=None,
    runtime_hooks=None,
    excludes=None,
    cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
    cipher=block_cipher)
exe = EXE(pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='ToolBox v1.1.0',
    debug=False,
    strip=False,
    upx=True,
    runtime_tmpdir=None,
    console=False ,
    icon='D:\\Python\\workspace_python\\ToolBox\\ui\\icon.ico')
