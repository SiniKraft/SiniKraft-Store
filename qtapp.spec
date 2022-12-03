# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['qtapp.py'],
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
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='SiniKraft-STORE',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
          version='file_version_info_sinikraft_store.txt', icon='SiniKraft-Store-icon.ico')

a_2 = Analysis(['update_checker.py'],
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
             noarchive=False)
pyz_2 = PYZ(a_2.pure, a_2.zipped_data,
             cipher=block_cipher)

exe_2 = EXE(pyz_2,
          a_2.scripts,
          [],
          exclude_binaries=True,
          name='Updater',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
          version='file_version_info_updater.txt', icon='SiniKraft-Store-icon.ico')

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               exe_2,
               a_2.binaries,
               a_2.zipfiles,
               a_2.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='SiniKraft-STORE')
