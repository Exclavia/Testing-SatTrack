import sys

from mods.data_info import SatelliteData
from mods.path_to import data_dir
from mods.gui import start_gui


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == '--help':
            print('\n  To start the satellite tracker, run this script without arguments.\n')
            print('    --help : Shows this message.')
            print('    --light : Runs the GUI in lightmode (Default darkmode)')
            print('    --force-dl : Forces a download, even if local keps exist and are within max days.')
        elif sys.argv[1] == '--force-dl':
            SatelliteData('amateur', data_dir(), force_dl=True)
        elif sys.argv[1] == '--light':
            start_gui(data_dir(), darkmode=False)
        else:
            print("That's not an option: --help for more information.")
    else:
        start_gui(data_dir())