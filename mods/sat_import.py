import os

from skyfield.api import load


def import_test ():
    print("sat_import.py imported succesfully.")

# Downloads Keplarian(Keps) Elements from Celestrak, only if file hasn't been download yet
# + only if previous file is more than max_days old (default 7.0)
def get_keps(sat_group:str, file_format:str, force_dl=False, max_days=7.0):
    """get_keps(sat_group: str -> Satellite group,
               file_format: str -> Format of the downloaded data,
               max_days: float -> Maximum amount of days before redownloading file (Default: 7.0)"""
    data_dir = os.path.join('..', 'data', 'keps')
    file_name = f"{sat_group}.{file_format}"
    # Check if data directory exists.
    if os.path.exists(data_dir):
        file_path = os.path.join(data_dir, file_name)
        u_base = "https://celestrak.org/NORAD/elements/gp.php"
        url = u_base + f"?GROUP={sat_group}&FORMAT={file_format}"
        if not load.exists(file_path) or load.days_old(file_path) >= max_days or force_dl:
            if force_dl: print("Downloading...")
            load.download(url, filename=file_path)
        return file_path

    print(f"{data_dir} does not exist.")
    return None


# Imports satinfo.txt and grabs additionally added satellite information.
def get_info():
    """Imports Satellite information via the satinfo.txt in the /data directory
Returns->list [ {
    "Name" : Satellite Name,
    "NORAD" : NORAD ID,
    "Uplink" : Uplink Frequency,
    "Downlink" : Downlink Frequency,
    "Mode" : Transmitter Mode  } ], ...
    """
    data_dir = os.path.join('..', 'data')
    sat_nfo = []
    with open(os.path.join(data_dir,'satinfo.txt'), "rt", encoding="utf-8") as info:
        info_list = info.read().split("\n")
        for nfo in info_list:
            nfo_list = nfo.split(";")
            sat_dict = {
                "Name": nfo_list[0],
                "NORAD": nfo_list[1],
                "Uplink": nfo_list[2],
                "Downlink": nfo_list[3],
                "Mode": nfo_list[4]
                }
            sat_nfo.append(sat_dict)

        return sat_nfo
