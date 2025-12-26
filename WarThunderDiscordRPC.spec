# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('configs', 'configs'), ('discord', 'discord'), ('game', 'game'), ('*.py', '.')],
    hiddenimports=['pypresence', 'requests', 'json', 'logging', 'importlib', 'importlib.util', 'importlib.machinery', 'configs.settings', 'configs.logs', 'configs.translations', 'configs.colors', 'game.api', 'discord.handler', 'discord.rpc', 'discord.init', 'discord.common', 'discord.types.map', 'discord.types.info', 'discord.types.air', 'discord.types.ground'],
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
    name='WarThunderDiscordRPC',
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
