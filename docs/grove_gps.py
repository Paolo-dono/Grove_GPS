#The GPS module used is a Grove GPS module http://www.seeedstudio.com/depot/Grove-GPS-p-959.html

import serial, time
from geopy.geocoders import Nominatim
import urllib.request
import json
import datetime
import math
    
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
            line = ser.readline()
            GPS.inp = line.decode('ISO-8859-1')
            #print(GPS.inp + "\n")
            if GPS.inp[0:6] =='$GPGGA': # GGA data for latitude, longitude, satellites, altitude, UTC position
                GPS.GGA = GPS.inp.split(",")
                if len(GPS.GGA) >= 10:
                    break
            time.sleep(0.1)     #needed by the cmd in order not to crash
        while True:
            GPS.inp2 = ser.readline().decode()
            if GPS.inp2[0:6] =='$GPRMC': # RMC data to get velocity
                GPS.RMC = GPS.inp2.split(",")
                if len(GPS.RMC) >= 8:
                    break
            time.sleep(0.1)
        
        #initialize values obtained from the GPS device
        
        if GPS.GGA[1] == '':
            ti = ""
        else:
            ti = GPS.GGA[1].split(".")[0]
            ti = ti[0:2] + ":" + ti[2:4] + ":" + ti[4:]  # convert to standard time format
        
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
        
        if GPS.GGA[7] == '': # number of satellites
            sats = 0
        else:
            sats = int(cleanstr(GPS.GGA[7]))
        
        if  GPS.GGA[9] == '': # altitude
            alt = -1.0
        else:
            alt = GPS.GGA[9]
        
        if GPS.RMC[7] == '': # speed
            spd = 0.0
        else:
            spd = 1.852*safefloat(GPS.RMC[7]) # conversion from knots to km/h
        
        GPS.values = [lat,lat_ns,long,long_ew,sats,alt,spd,ti]
    
    # Accessor methods for all the desired GPS values
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
    def getUTCPosition(self):
        return GPS.values[7]
        
if __name__ == "__main__":
    gps = GPS()
    
    # if all the folowing outputs have values,
    # it show the GPS module was able to connect to the satellites properly
    print("Latitude: " + str(gps.getLatitude()))
    print("Longitude: " + str(gps.getLongitude()))
    print("Number of satellites: " + str(gps.getSatellites()))
    print("UTC position: " + gps.getUTCPosition())
    
    def getCoordinatesFromAddress(self, address):
        api_key = "AIzaSyBye-KERYIXDd24hk0C19mSMXdS7TmCX3M"
        address = address.replace(" ", "+")
        link = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}".format(address, api_key)
        response = urllib.request.urlopen(link).read()
        data = json.loads(response)
        latitude = data["results"][0]["geometry"]["location"]["lat"]
        longitude = data["results"][0]["geometry"]["location"]["lng"]
        return [latitude, longitude]
    
    def distance(self, lat1, lng1, lat2, lng2):
        degtorad = math.pi/180
        dLat = (lat1-lat2)*degtorad
        dLng = (lng1-lng2)*degtorad
        a = pow(math.sin(dLat/2), 2) + math.cos(lat1*degtorad)*math.cos(lat2*degtorad)*pow(math.sin(dLng/2), 2)
        b = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
        return 6371*b
    
    def distanceToHome(self):
        f = open("home.txt", "r")
        home = f.readlines()[0]
        f.close()
        lat, lng = g.getCoordinatesFromAddress(home)
        g.refresh()
        lat2 = g.getLatitude()
        lng2 = g.getLongitude()
        return self.distance(lat, lng, lat2, lng2)
    
    def setHomeAddress(self, address):
        f = open("home.txt", "w")
        f.write(home)
        f.close()
    
    def getHomeAddress(self):
        f = open("home.txt", "r")
        a = f.readlines()
        return a[0]
    
    def logLocation(self):
        time_start = time.time()
        dt = datetime.datetime.now()
        address1 = self.getAddress()
        h = open("history.txt", "a")
        h.write(str(dt1) + "\n")
        h.write(address1 + "\n")
        h.close()
        while True:
            address2 = self.getAddress()
            if address1 != address2:
                time_elapsed = time.time() - time_start
                if time_elapsed > 600:
                    favourites = open("favourites.txt")
                    fav = json.load(favourites)
                    favourites.close()
                    if address2 in fav:
                        fav[address2] += 1
                    else:
                        fav[address2] = 1
                    new_favourites = open("favourites.txt", "w")
                    json.dump(fav, new_favourites)
                    new_favourites.close()
                dt = datetime.datetime.now()
                f = open("history.txt", "a")
                f.write(str(dt) + "\n")
                f.write(address2 + "\n")
                f.close()
                address1 = address2
                time_start = time.time()
            time.sleep(60)
    
    def getFavouriteLocations(self):
        favourites = open("favourites.txt")
        fav = json.load(favourites)
        favourites.close()
        top = []
        for i in range(5):
            highest = 0
            place = ""
            for j in fav:
                if fav[j] > highest:
                    highest = fav[j]
                    place = j
            fav.pop(place)
            top.append(place)
        return top
    
    def locationAtTime(self, dt):
        f = open("history.txt", "r")
        data = f.readlines()
        f.close()
        start = 0
        stop = len(data)
        found = False
        address = ""
        while found == False:
            pos = (stop - start)//2 + start
            if pos%2 == 1:
                pos-=1
            if dt < data[pos][:19]:
                stop = pos
            else:
                start = pos
            if (stop - start) == 2:
                found = True
                address = data[pos+1]
        return address
    
    def timesAtLocation(self, address):
        favourites = open("favourites.txt")
        fav = json.load(favourites)
        favourites.close()
        return fav[address]
        
        
if __name__ == "__main__":
    g = GPS_Extension()
    #print(g.getCoordinatesFromAddress("19 Loots Road Blairgowrie, Randburg"))
    #print(g.distance(-26.103062, 28.003815, -26.116043, 28.001292))
    #print(g.locationAtTime("2020-10-13 20:22:14.850905"))
    #print(g.timesAtLocation("address3"))
    
#     f = open("history.txt", "a")
#     f.write(str(datetime.datetime.now()) + "\n")
#     f.write("9 Loots Road Blairgowrie, Randburg\n")
#     f.close()
