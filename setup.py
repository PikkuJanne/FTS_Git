from cx_Freeze import setup, Executable
import os

# Include any necessary files here (e.g., images, sounds)
includes = []
include_files = [
    'fts.ico', 
    'background1.png', 
    'cross1.png', 
    'main_menu.png', 
    'about.png', 
    'PIMEÄSAMMAKKO-Enochian_19_Avainta.mp3',
    'enemy.py', 
    'game.py', 
    'game_object.py', 
    'player.py',
    'corpse_mask15.png',
    'sun1.png',
    'ZombieAttack05.mp3',
    'ZombieMoan01.mp3'
]

# Define the main script that will be run when the executable is launched
main_script = 'fuck_the_sun.py'

# Specify the base for the executable. Use "Win32GUI" for Windows GUI applications.
base = None

# Set the executable options
exe_options = {
    'includes': includes,
    'include_files': include_files,
}

# Define the executables
executables = [
    Executable(main_script, base=base, icon='fts.ico')
]

# Set the setup options
setup_options = {
    'name': 'FUCK THE SUN',
    'version': '0.1',
    'description': 'Balck Metal acion game',
    'executables': executables,
    'options': {'build_exe': exe_options}
}

# Run the setup
setup(**setup_options)
