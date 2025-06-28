from os import path


def import_test ():
    print("get_sat.py imported succesfully.")


def data_dir():
    if path.exists("..\\data"): data_dir = "..\\data"
    elif path.exists(".\\data"): data_dir = ".\\data"
    else: raise NotADirectoryError("No data directory found")
    return data_dir
