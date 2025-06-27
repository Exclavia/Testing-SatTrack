import sys
from mods.get_keps import get_keps
from mods.gui import start_gui

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == '--force-dl':
            f_p = get_keps('amateur', 'csv', force_dl=True)
            print(f"File downloaded to: {f_p}")
        else: print("Not an option.")
    else:
        start_gui()
