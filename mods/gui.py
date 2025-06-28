import tkinter as tk
from tkinter import ttk, messagebox, BOTH, PhotoImage
from tkinter.font import Font
from ttkbootstrap import Style
try:
    from get_sat import GetSat
    from data_info import SatelliteData
    from display import disp_data
except ImportError:
    from mods.get_sat import GetSat
    from mods.data_info import SatelliteData
    from mods.display import disp_data

def import_test ():
    print("gui.py imported succesfully.")

def start_gui(d_path:str, darkmode=True):
    """Main GUI function"""
    # Grabbing satellite info from data/satinfo.txt
    sd = SatelliteData('amateur', d_path)
    sat_import = sd.add_info
    sat_options = []
    # Adds to list for combo box options
    for nfo in sat_import:
        sat_options.append(f"{nfo.get('Name')}: {nfo.get('NORAD')}")


    def show_selected_item(in_lat:float, in_lon:float, min_elev:float):
        """Calls getSat function and displays returned data"""
        selected_item = combo_box.get()
        if selected_item:
            sat_sep = selected_item.replace(" ", "").split(":")
            norad = int(sat_sep[1])
            name = sat_sep[0]
            sat_data = GetSat(norad, in_lat, in_lon, min_elev, d_path).data
            combo_box.set(selected_item)
            # Setting variables from getSat
            risd = sat_data[1].get("Elev"), sat_data[1].get("Distance"), sat_data[1].get("When")
            clmd = sat_data[2].get("Elev"), sat_data[2].get("Distance"), sat_data[2].get("When")
            setd =  sat_data[3].get("Elev"), sat_data[3].get("Distance"), sat_data[3].get("When")
            info = sat_data[4].get("Uplink"), sat_data[4].get("Downlink"), sat_data[4].get("Mode")
            # Displayed Info ================
            ds_list = disp_data(name, norad, in_lat, in_lon, info, risd, clmd, setd)
            for line in ds_list:
                text_area.insert(tk.INSERT, line)
            text_area.config(state=tk.DISABLED)


    def button_click():
        """Button command function"""
        # Check if Lat/Lon is entered & if Satellite is selected
        if lat_entry.get() == "" or long_entry.get() == "":
            messagebox.showinfo("Coordinates", "You have to enter coordinates.")
        elif combo_box.get() == "Select a Satellite":
            messagebox.showinfo("Satellite selection", "Please select a satellite.")
        elif elev_entry.get() == "":
            messagebox.showinfo("Minimum Elevation", "Please enter a minimum elevation.")
        else:
            text_area.config(state=tk.NORMAL)
            text_area.delete('1.0', tk.END)
            e_lat = float(lat_entry.get())
            e_lon = float(long_entry.get())
            e_ele = float(elev_entry.get())
            show_selected_item(in_lat=e_lat, in_lon=e_lon, min_elev=e_ele)

    # Create the main application window
    root = tk.Tk()
    img = PhotoImage(file='images/icon.png')
    root.iconphoto(False, img)
    root.title("Satellite Tracker")
    root.resizable(False, False)
    root.geometry("360x650")
    font = Font(family="Arial", size=20)
    root.option_add("*TCombobox*Listbox*Font", font)
    if darkmode: Style(theme='darkly') # Enables dark theme

    # === LAT/LONG/MIN.ELEV ENTRY FIELDS ===
    entry_frame = ttk.Frame(root)
    entry_frame.pack(pady=8, padx=10, fill='x')
    # Lat
    lat_label = ttk.Label(entry_frame, text="Latitude")
    lat_label.grid(row=0, column=0, sticky='w', padx=8)
    lat_entry = ttk.Entry(entry_frame, width=35)
    lat_entry.grid(row=1, column=0, padx=8)
    # Lon
    long_label = ttk.Label(entry_frame, text="Longitude")
    long_label.grid(row=2, column=0, sticky='w', padx=8)
    long_entry = ttk.Entry(entry_frame, width=35)
    long_entry.grid(row=3, column=0, padx=8)
    # Min. Elevation
    elev_label = ttk.Label(entry_frame, text="Min Elevation")
    elev_label.grid(row=1, column=1, sticky='w', padx=8)
    elev_entry = ttk.Entry(entry_frame, width=10)
    elev_entry.grid(row=2, column=1, padx=8)
    elev_entry.insert(tk.INSERT, "20.0")

    # === SATELLITE DROPDOWN ===
    combo_box = ttk.Combobox(root, values=sat_options, width=20, font=("Arial", 18), state="readonly")
    combo_box.set("Select a Satellite")
    combo_box.pack(pady=5, padx=8, fill=BOTH)

    # === OUTPUT TEXT BOX ===
    text_area = tk.Text(root, width=36, height=22, font=("Arial", 12), state=tk.DISABLED)
    text_area.pack(padx=2, pady=10)
    submitbutton = tk.Button(root, text="Lookup Satellite", command=button_click, font=("Arial", 12))
    submitbutton.pack(padx=8, pady=5, fill=BOTH)

    # Run the Tkinter event loop
    root.mainloop()
