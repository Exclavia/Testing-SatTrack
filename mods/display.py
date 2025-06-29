
def disp_data(nnll, info, rise, culm, sets):
    """Returns displayed text information as list"""
    display_list = [f"  Name: {nnll[0]}",
                    f"\n  NORAD: {nnll[1]}\n",
                    f"  Lat: {nnll[2]} | Lon: {nnll[3]}\n",
                    f"  Up: {info[0]}  |  Down: {info[1]}\n",
                    f"  Mode: {info[2]}\n",
                    "____________ Next Pass ___________" + "\n\n",
                    f" ● Rise\n  | Elevation: {rise[0]}\n  | Distance: {rise[1]}\n  | When: {rise[2]}\n\n",
                    f" ● Max\n  | Elevation: {culm[0]}\n  | Distance: {culm[1]}\n  | When: {culm[2]}\n\n",
                    f" ● Set\n  | Elevation: {sets[0]}\n  | Distance: {sets[1]}\n  | When: {sets[2]}"]
    return display_list
