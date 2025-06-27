import os

# Imports satinfo.txt and grabs additionally added satellite information.
def import_satellites():
    """Imports Satellite information via the satinfo.txt in the /data directory
Returns->list [ {
    "Name" : Satellite Name,
    "NORAD" : NORAD ID,
    "Uplink" : Uplink Frequency,
    "Downlink" : Downlink Frequency,
    "Mode" : Transmitter Mode  } ], ...
    """
    data_dir = os.path.join('.', 'data')
    sat_info = []
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
            sat_info.append(sat_dict)

        return sat_info
