from time import time
from datetime import datetime as dt
from csv import DictReader

from skyfield.api import wgs84, load, Timescale
from skyfield.api import EarthSatellite as es
from pytz import timezone as py_tz

try:
    from data_info import SatelliteData
    from path_to import data_dir
except ImportError:
    from mods.data_info import SatelliteData
    from mods.path_to import data_dir


_path = data_dir()
class GetSat:
    """Takes NORAD Number, Latitude, Longitude, Minimum elevation and data directory path, returns Satellite descripton info and rise, culmination and set data."""
    def __init__(self, norad:int, latitude:float, longitude:float, min_elevation:float):
        self.path = _path
        self.norad = norad
        self.lat = latitude
        self.lon = longitude
        self.min = min_elevation
        self.data = self.__getsat__()

    def _24(self, epoch):
        return epoch + 86400.0

    def _ts(self, ts:Timescale, dt0, dt1):
        return ts.from_datetime(dt0), ts.from_datetime(dt1)

    def _dt(self, t0, t1, tzn):
        return dt.fromtimestamp(t0, tz=tzn), dt.fromtimestamp(t1, tz=tzn)
    # Function loads local keps file, reads it, calculates, returns in list/dict
    def __getsat__(self):
        sd = SatelliteData('amateur')
        # Using parsed kep-data to make a few lists to allow easier access to the information.
        sat_info = []
        sat_import = sd.add_info
        file_path = sd.csv_path
        with load.open(file_path, mode='r') as f:
            data = list(DictReader(f))
        tz = py_tz('America/Detroit')
        # Setting Timescale/Datetime/Timezone
        ts = load.timescale()
        d0, d1 = self._dt(time(), self._24(time()), tz)
        t0, t1 = self._ts(ts, d0, d1)
        earth_sats = [es.from_omm(ts, fields) for fields in data]
        by_number = {sat.model.satnum: sat for sat in earth_sats}
        main_sat = by_number[self.norad]
        pos = wgs84.latlon(self.lat, self.lon)
        for sat in earth_sats:
            if sat.model.satnum == self.norad:
                sat_info.append({"Name": sat.name, "NORAD": sat.model.satnum})
        # Finding events using the two set timescales (Current time + 24hours)
        t, sat_events = main_sat.find_events(pos, t0, t1, altitude_degrees=self.min)
        event_names = 'Rises', 'Culminates', 'Sets'
        pass_limit = 1
        format_str = "%b %d, %Y at %I:%M:%S %p"
        # For loop to loop through data and grab only what we want based on pass_limit
        # Default: Next pass that rises above set min. elevation
        # Returns Rise/Max/Set elevation, datetime and satellite distance (in miles)
        for ti, event in zip(t, sat_events):
            utc_datetime = ti.astimezone(tz)
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
            if int(more.get("NORAD")) != self.norad: continue
            more_dict = {
                "Uplink": more.get("Uplink"),
                "Downlink": more.get("Downlink"),
                "Mode": more.get("Mode")
                }
            sat_info.append(more_dict)
        return sat_info
