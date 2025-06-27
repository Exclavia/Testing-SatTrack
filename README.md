# Satellite tracker
![pylint](https://img.shields.io/badge/PyLint-10.00-brightgreen?logo=python&logoColor=white)

Simple satellite tracker with a GUI that shows the next pass for a selected satellite over a given longitude and latitude based on minimum elevation.

<img src="https://raw.githubusercontent.com/Exclavia/Satellite-Tracker/refs/heads/main/images/screenshot.png"/>

No longer dependent on a third-party API, this program will download and store Keplarian elements from Celestrak automatically and regularly based on how long since last download. Now using the Skyfield module in order to calulate satellite position, elevation and distance with the downloaded keps. 


## How to use
Program can be ran by running the `main.py` script. Once opened, you have to input your latitude, longitude and select a satellite, by default minimum elevation input is set to 20.0 degrees, but can be changed to be higher or lower.
Be careful though I haven't added any sort of checks to make sure you don't input a value to high or low (For lat/lon -200 wouldn't make sense. vice versa)


## Satellites
Can be changed and added based on the keps satellite group selected, unfortunately additional satellite information (Uplink, Downlink, Mode) is still based on the local satinfo.txt
Some of the satellites in the satinfo.txt may return errors, as I only grabbed and formatted the currently listed active radio satellites from AMSAT, and some of them aren't in the "amateur" satellite group keps elements (For some reason?)
There are still more plans to be able to hopefully grab this information and be able to list the satellites based on what elements have been downloaded, rather than what additional information is stored.


## External Usage
Originally it was more setup as either CLI or GUI, but I pivoted the program more to the GUI, you can still call the get_sats() function, but rather than any built-in console printlines, all the information is just returned in list/dicts.
See the `gui.py` file to see how to implement it yourself, it's fairly straight forward at the moment.

