==================================
Grove GPS
==================================

API for the Seeed Studio Grove GPS connected to a Raspberry Pi.

* GitHub repo: https://github.com/Paolo-dono/Grove_GPS
* Free software: MIT License

Connecting the GPS module to the Raspberry Pi:

  Format: [GPS module pin] -> [Raspberry Pi pin]

  * Vcc -> 3.3V
  * Rx -> Tx (GPIO 14, board pin 8)
  * Tx -> Rx (GPIO 15, board pin 10)
  * GND -> GND

Setup to use API:

* Enable UART communication using raspi-config
* Run the following commands:
  
  * pip3 install datetime
  * pip3 install pyserial
  * pip3 install groveGPS
  
* Then to use the code in a python file add the following code at the top of the program:
  
  * from location_calcs import location_calcs
  * from grove_gps import GPS

Setup to use location_calcs:

* Get a Google API key and pass it into the setAPIkey() method to get the full functionality of the class

Methods of GPS class:

+ GPS() -> instantiates an object of the class and calls the refresh() method

+ refresh() -> fetches new values from the GPS module

+ getLatitude(): float -> returns the latitude in decimal format

+ getLongitude(): float -> returns the longitude in decimal format

+ getNS(): String -> returns whether the latitude is North or South

+ getWE(): String -> returns whether the longitude is West or East

+ getSatellites(): int -> returns the number of satellites the GPS module is connected to

+ getSpeed(): float -> returns the speed in km/h

+ getUTCPosition(): String -> returns the current UTC time

Methods of the location_calcs class:

+ location_calcs() -> creates an obect of the class, instantiates a local GPS object and sets the default refresh rate

+ setAPIkey(String key) -> sets a new Google Maps API key 

+ getAPIkey() -> returns current API key

+ getCurrentAddress(): String -> returns current street address from coordinates fetched from the GPS module

+ getAddressFromCoordinates(float latitiude, float longitude): String -> returns the street address given a set of coordinates

+ getCoordinatesFromAddress(String address): float list -> returns a set of coordinates given a street address

+ setHomeAddress(String address) -> sets a home address and stores it in a text file

+ getHomeAddress(): String -> returns the home address stored in a text file

+ setRefreshRate(int refresh_rate) -> sets a new refresh rate

+ getRefreshRate(): int -> returns current refresh rate

+ getDistanceToHome(): float -> returns the distance you are from the set home address in kilometres

+ getDistance(float latitude1, float longitude1, float latitude2, float longitude2): float -> returns the distance between two sets of coordinates

+ logLocation() -> creates a history log of all locations you have visited and routes you drove in a text file

+ locationAtTime(String dateAndTime): String -> returns the location you were at a certain time

+ timesAtLocation(String address): String list -> returns the number of times you visited a location

+ getFavouriteLocations(): String list -> returns a list of the top 5 locations you visited the most

Known bugs

* The Grove GPS can often struggle to connect with satellites. If you see it is struggling, you must take it outside under the open sky (and only turn it on when you are outside) and then wait for at least half a minute before moving indoors

* When running the logLocation() method the GPS values that are fetched can get frozen and show you are staying in the same position even when driving around

Acknowledgements:

* Code from Dexter Industries: https://github.com/DexterInd/GrovePi/blob/master/Software/Python/grove_gps/grove_gps_data.py
