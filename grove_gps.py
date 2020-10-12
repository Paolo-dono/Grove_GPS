import serial, time
from geopy.geocoders import Nominatim
import urllib.request
import json
import datetime
    
ser = serial.Serial('/dev/ttyAMA0',  9600, timeout = 0)
ser.flush()

def cleanstr(in_str):
    out_str = "".join([c for c in in_str if c in "0123456789.-" ])
    if len(out_str)==0:
        out_str = "-1"
    return out_str

def safefloat(in_str):
    try:
        out_str = float(in_str)
    except ValueError:
        out_str = -1.0
    return out_str

# Convert to decimal degrees
def decimal_degrees(raw_degrees):
    try:
        degrees = float(raw_degrees) // 100
        d = float(raw_degrees) % 100 / 60
        return degrees + d
    except: 
        return raw_degrees

class GPS:
    #The GPS module used is a Grove GPS module http://www.seeedstudio.com/depot/Grove-GPS-p-959.html
    inp = []
    inp2 = []
    # Refer to SIM28 NMEA spec file http://www.seeedstudio.com/wiki/images/a/a0/SIM28_DATA_File.zip
    GGA = []
    RMC = []
    values = []
    home = ""
    
    def __init__(self):
        self.refresh()
    
    #Read data from the GPS
    def refresh(self): 
        while True:
            GPS.inp = ser.readline().decode()
            print(GPS.inp)
            if GPS.inp[0:6] =='$GPGGA': # GGA data , packet 1, has all the data we need
                GPS.GGA = GPS.inp.split(",")
                if len(GPS.GGA) >= 10:
                    break
            time.sleep(0.1)     #without the cmd program will crash
        while True:
            GPS.inp2 = ser.readline().decode()
            if GPS.inp2[0:6] =='$GPRMC': # GGA data , packet 1, has all the data we need
                GPS.RMC = GPS.inp2.split(",")
                if len(GPS.RMC) >= 8:
                    break
            time.sleep(0.1)
        
        #initialize values obtained from the GPS device
        
        if GPS.GGA[2] == '':  # latitude. Technically a float
            lat =-1.0
        else:
            lat = decimal_degrees(safefloat(cleanstr(GPS.GGA[2])))
        
        if GPS.GGA[3] == '':  # this should be either N or S
            lat_ns = ""
        else:
            lat_ns=str(GPS.GGA[3])
        if lat_ns == "S":
            lat = -lat
            
        if  GPS.GGA[4] == '':  # longitude. Technically a float
            long = -1.0
        else:
            long = decimal_degrees(safefloat(cleanstr(GPS.GGA[4])))
        
        if  GPS.GGA[5] == '': # this should be either W or E
            long_ew = ""
        else:
            long_ew = str(GPS.GGA[5])
        if long_ew == "W":
            long = -long
        
        sats = int(cleanstr(GPS.GGA[7]))
        
        if  GPS.GGA[9] == '':
            alt = -1.0
        else:
            alt = GPS.GGA[9]
        
        if GPS.RMC[7] == '':
            spd = 0.0
        else:
            spd = 1.852*safefloat(GPS.RMC[7])
        
        GPS.values = [lat,lat_ns,long,long_ew,sats,alt,spd]
    
    def getAddress(self):
        api_key = "AIzaSyBye-KERYIXDd24hk0C19mSMXdS7TmCX3M"
        coordinates = str(GPS.values[0]) + "," + str(GPS.values[2])
        link = "https://maps.googleapis.com/maps/api/geocode/json?latlng={}&key={}".format(coordinates, api_key)
        response = urllib.request.urlopen(link).read()
        address = json.loads(response)["results"][0]["formatted_address"]
        return address
    
    def getAddress(self, lat, long):
        api_key = "AIzaSyBye-KERYIXDd24hk0C19mSMXdS7TmCX3M"
        coordinates = str(lat) + "," + str(long)
        link = "https://maps.googleapis.com/maps/api/geocode/json?latlng={}&key={}".format(coordinates, api_key)
        response = urllib.request.urlopen(link).read()
        address = json.loads(response)["results"][0]["formatted_address"]
        return address

    def getLatitude(self):
        return GPS.values[0]
    def getNS(self):
        return GPS.values[1]
    def getLongitude(self):
        return GPS.values[2]
    def getEW(self):
        return GPS.values[3]
    def getSatellites(self):
        return GPS.values[4]
    def getAltitude(self):
        return GPS.values[5]
    def getSpeed(self):
        return GPS.values[6]
    
    def setHomeAddress(self, address):
        GPS.home = address
        f = open("home.txt", "w")
        f.write(address + "\n")
        f.close()
    
    def getHomeAddress(self):
        return GPS.home
    
    def logLocation(self):
        while True:
            dt1 = str(datetime.datetime.now())
            self.refresh()
            address1 = self.getAddress(self.getLatitude(), self.getLongitude())
            time.sleep(240)
            self.refresh()
            address2 = self.getAddress(self.getLatitude(), self.getLongitude())
            if address1 == address2:
                f = open("history.txt", "a")
                f.write(dt1 + "\n")
                f.write(address2 + "\n")
                f.close()
                favourites = open("favourites.txt")
                fav = json.load(favourites)
                favourites.close()
                if address1 in fav:
                    fav[address1] += 1
                else:
                    fav[address1] = 1
                new_favourites = open("favourites.txt", "w")
                json.dump(fav, new_favourites)
                new_favourites.close()
    
    def getFavouriteLocations(self):
        
            
            
            
            
            
            
            
