import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["pygame"], "include_files" : ["Textures/buttonCheck.png", "Textures/buttonLock.png", "Textures/menuBg.png", "Textures/messageSelection.png", "Textures/ZoneDepart.png", "Textures/ZoneDessin.png", "Textures/icone.png"]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"


setup(  name = "Tangram",
    version = "1.0",
    description = "Tangram IA",
    options = {"build_exe": build_exe_options},
    executables = [Executable("Main.py", base = base)])