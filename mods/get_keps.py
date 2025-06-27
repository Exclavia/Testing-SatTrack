import os
from skyfield.api import load

# Downloads Keplarian(Keps) Elements from Celestrak, only if file hasn't been download yet
# + only if previous file is more than max_days old (default 7.0)
def get_keps(sat_group:str, file_format:str, force_dl=False, max_days=7.0):
    """get_keps(sat_group: str -> Satellite group,
               file_format: str -> Format of the downloaded data,
               max_days: float -> Maximum amount of days before redownloading file (Default: 7.0)"""
    data_dir = os.path.join('.', 'data', 'keps')
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
