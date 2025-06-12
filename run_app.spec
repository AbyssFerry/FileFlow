# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_dynamic_libs, collect_data_files, collect_submodules
import pdfplumber
import os

# 主程序用到的数据库文件
datas = [('fileflow_database.db', '.')]

# 自动收集常用库的动态链接库
binaries = (
    collect_dynamic_libs('numpy') +
    collect_dynamic_libs('PyQt5') +
    collect_dynamic_libs('lxml') +
    collect_dynamic_libs('cryptography')
)


# 收集 PyQt5 和 lxml 的资源文件
datas += collect_data_files('lxml')
datas += collect_data_files('PyQt5')

# ✅ 手动添加 pdfplumber 所在目录下的所有 .py 文件为数据（如果默认方法失败）
pdfplumber_dir = os.path.dirname(pdfplumber.__file__)
for fname in os.listdir(pdfplumber_dir):
    if fname.endswith(".py"):
        datas.append((os.path.join(pdfplumber_dir, fname), os.path.join('pdfplumber', fname)))

# ✅ 收集 pdfplumber 子模块
hiddenimports = collect_submodules('pdfplumber')

# 收集 pdfminer 子模块
hiddenimports += collect_submodules('pdfminer')

# 其他必须显式列出的包
hiddenimports += [
    'numpy',
    'pandas',
    'PyQt5.QtWidgets',
    'PyQt5.QtGui',
    'PyQt5.QtCore',
    'lxml',
]

a = Analysis(
    ['run_app.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='FileFlow',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    icon='res/icon.png',
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
