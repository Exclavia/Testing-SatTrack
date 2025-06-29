from os import path
from csv import DictReader

from skyfield.api import load
try:
    from path_to import data_dir
except ImportError:
    from mods.path_to import data_dir

def import_test ():
    print("data_info.py imported succesfully.")


class SatelliteData:
    """ Takes Celestrak satellite group and data directory path + Optional force download and max amount of days before downloading again."""
    def __init__ (self, sat_group:str, force_dl=False, max_days=7.0):
        self.group = sat_group
        self.data_path = data_dir()
        self.force = force_dl
        self.max = max_days
        self.csv_path = self.getkeps()
        self.add_info = self.__addinfo__(self.data_path, self.csv_path)

    # Imports satinfo.txt and grabs additionally added satellite information.
    def __addinfo__(self, d_dir, csv_path):
        sat_info = []
        with open(path.join(d_dir,'satinfo.txt'), 'rt', encoding='utf-8') as info:
            info_list = info.read().split("\n")
            col = "NORAD_CAT_ID"
            with open(csv_path, mode='r', newline='', encoding='utf-8') as f:
                csv_data = DictReader(f)
                for row in csv_data:
                    for nfo in info_list:
                        nfo_list = nfo.split(";")
                        if int(nfo_list[1]) == int(row[col]):
                            sat_dict = {
                                "Name": nfo_list[0],
                                "NORAD": nfo_list[1],
                                "Uplink": nfo_list[2],
                                "Downlink": nfo_list[3],
                                "Mode": nfo_list[4]
                                }
                            sat_info.append(sat_dict)
            return sat_info


    # Downloads keps from Celestrak if file doesn't exist or current file is more than max_days old
    def getkeps(self):
        """get_keps(sat_group: str -> Satellite group,
                   file_format: str -> Format of the downloaded data,
                   max_days: float -> Maximum amount of days before redownloading file (Default: 7.0)"""
        file_name = f"{self.group}.csv"
        # Check if data directory exists.
        if path.exists(self.data_path):
            file_path = path.join(self.data_path, file_name)
            u_base = "https://celestrak.org/NORAD/elements/gp.php"
            url = u_base + f"?GROUP={self.group}&FORMAT=CSV"
            if not load.exists(file_path) or load.days_old(file_path) >= self.max or self.force:
                if self.force: print("Downloading...")
                load.download(url, filename=file_path)
            return file_path

        print(f"{self.data_path} does not exist.")
        return None
