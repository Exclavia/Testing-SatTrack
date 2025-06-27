from csv import DictReader
from time import time
from datetime import datetime as dt
from skyfield.api import EarthSatellite, wgs84, load
from pytz import timezone as py_tz
from mods.import_sat import import_satellites
from mods.get_keps import get_keps

# Function loads local keps file, reads it, calculates, returns in list/dict
def get_sat(norad_id:int, usr_lat:float, usr_lon:float, usr_minalt:float):
    """get_sat(norad_id: int -> NORAD ID,
               usr_lat: float -> Latitude,
               usr_lon: float -> Longitude,
               usr_minalt: float -> Minimum elevation/altitude"""
    sat_import = import_satellites()
    file_path = get_keps(sat_group='amateur', file_format='csv')
    with load.open(file_path, mode='r') as f:
        data = list(DictReader(f))
    # Setting Timescale/Datetime/Timezone
    ts = load.timescale()
    l_tz = py_tz('America/Detroit')
    t0 = ts.from_datetime(dt.fromtimestamp(time(), tz=l_tz))
    ep_24 = time() + 86400.00
    t1 = ts.from_datetime(dt.fromtimestamp(ep_24, tz=l_tz))
    # Parsing Keps and returning easily callable data.
    earth_sats = [EarthSatellite.from_omm(ts, fields) for fields in data]
    by_number = {sat.model.satnum: sat for sat in earth_sats}
    main_sat = by_number[norad_id]
    pos = wgs84.latlon(usr_lat, usr_lon)
    # Using parsed kep-data to make a few lists to allow easier access to the information.
    sat_data = []
    sat_info = []
    for sat in earth_sats:
        if sat.model.satnum == norad_id:
            sat_info.append(sat.name)
        sat_dict = {
            "Name": sat.name,
            "NORAD": sat.model.satnum
            }
        sat_data.append(sat_dict)
    # Finding events using the two set timescales (Current time + 24hours)
    t, sat_events = main_sat.find_events(pos, t0, t1, altitude_degrees=usr_minalt)
    event_names = 'Rises', 'Culminates', 'Sets'
    pass_limit = 1
    format_str = "%b %d, %Y at %I:%M:%S %p"
    # For loop to loop through data and grab only what we want based on pass_limit
    # Default: Next pass that rises above set min. elevation
    # Returns Rise/Max/Set elevation, datetime and satellite distance (in miles)
    for ti, event in zip(t, sat_events):
        utc_datetime = ti.astimezone(l_tz)
        dt_fm = utc_datetime.strftime(format_str)
        pos_diff = main_sat - pos
        alt, _, dx = pos_diff.at(ti).altaz()
        km_mile = float(dx.km) * 0.621371
        pass_dict = {
            "Event": f"{event_names[event]}",
            "When": f"{dt_fm}",
            "Elev": f"{str(alt)[:2]}°",
            "Distance": f"{str(km_mile)[:6]}mi"
        }
        sat_info.append(pass_dict)
        if pass_limit == 3: break
        pass_limit = pass_limit + 1
    # Scans through satinfo.txt, finds inputted NORAD, returns additional information
    # Uplink frequency, Downlink frequency, Transmitter mode.
    for more in sat_import:
        if int(more.get("NORAD")) != norad_id: continue
        more_dict = {
            "Uplink": more.get("Uplink"),
            "Downlink": more.get("Downlink"),
            "Mode": more.get("Mode")
            }
        sat_info.append(more_dict)
    return sat_info
