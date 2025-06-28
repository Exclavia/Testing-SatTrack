from csv import DictReader
from time import time
from datetime import datetime as dt
from skyfield.api import wgs84, load, Timescale
from skyfield.api import EarthSatellite as es
from pytz import timezone as py_tz
try:
    from data_info import SatelliteData
except:
    from mods.data_info import SatelliteData

def import_test ():
    print("get_sat.py imported succesfully.")
class GetSat:
    def __init__(self, norad:int, latitude:float, longitude:float, min_elevation:float, data_path:str):
        self.data = self.__getsat__(norad, latitude, longitude, min_elevation, data_path)
        
    def _24(self, epoch):
        return epoch + 86400.0
    
    def dt2(self, ts:Timescale, dtime):
        return ts.from_datetime(dtime)
    
    def ts2(self, times, tzone):
        return dt.fromtimestamp(times, tz=tzone)
    
    # Function loads local keps file, reads it, calculates, returns in list/dict
    def __getsat__(self, norad:int, lat:float, lon:float, minel:float, datapath:str):
        sd = SatelliteData('amateur', datapath)
        """get_sat(norad: int->NORAD, lat: float->Latitude, lon: float->Longitude, minel: float->Min. elevation"""
        # Using parsed kep-data to make a few lists to allow easier access to the information.
        sat_data = []
        sat_info = []
        sat_import = sd.add_info
        file_path = sd.csv_path
        with load.open(file_path, mode='r') as f:
            data = list(DictReader(f))
        tz = py_tz('America/Detroit')
        # Setting Timescale/Datetime/Timezone
        ts = load.timescale()
        d0, d1 = self.ts2(time(), tz), self.ts2(self._24(time()), tz)
        t0, t1 = self.dt2(ts, d0), self.dt2(ts, d1)
        # Parsing Keps and returning easily callable data.
        earth_sats = [es.from_omm(ts, fields) for fields in data]
        by_number = {sat.model.satnum: sat for sat in earth_sats}
        main_sat = by_number[norad]
        pos = wgs84.latlon(lat, lon)
        for sat in earth_sats:
            if sat.model.satnum == norad:
                sat_info.append(sat.name)
            sat_dict = {
                "Name": sat.name,
                "NORAD": sat.model.satnum
                }
            sat_data.append(sat_dict)
        # Finding events using the two set timescales (Current time + 24hours)
        t, sat_events = main_sat.find_events(pos, t0, t1, altitude_degrees=minel)
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
            if int(more.get("NORAD")) != norad: continue
            more_dict = {
                "Uplink": more.get("Uplink"),
                "Downlink": more.get("Downlink"),
                "Mode": more.get("Mode")
                }
            sat_info.append(more_dict)
        return sat_info
