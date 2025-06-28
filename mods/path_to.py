from os import path


def import_test ():
    print("get_sat.py imported succesfully.")


def data_dir():
    if path.exists("..\\data"): data = "..\\data"
    elif path.exists(".\\data"): data = ".\\data"
    else: raise NotADirectoryError("No data directory found")
    return data
