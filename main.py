from mods.path_to import data_dir
from mods.gui import start_gui

data_directory = data_dir()

if __name__ == "__main__":
    start_gui(data_directory)