from grove_gps import GPS
import time, datetime
import json
import math
import urllib.request

class location_calcs:
    g = None
    refresh = 30
    
    def __init__(self): # initialises the global variables
        global g
        global refresh
        
        g = GPS()
        refresh = 30
    
    def getLogRefreshRate(self): # returns the rate at which new locations are added 
        global refresh           # to the history log of locations visited
        return refresh
    
    def setLogRefreshRate(self, new_refresh): # sets a new refresh rate for the history log
        global refresh
        refresh = new_refresh
    
    def getCurrentAddress(self): # performs reverse geocoding to return the current street address
        global g                 # from the coordinates read from the GPS module
        
        g.refresh()
        api_key = "AIzaSyBye-KERYIXDd24hk0C19mSMXdS7TmCX3M"
        coordinates = str(g.getLatitude()) + "," + str(g.getLongitude())
        link = "https://maps.googleapis.com/maps/api/geocode/json?latlng={}&key={}".format(coordinates, api_key)
        response = urllib.request.urlopen(link).read()
        address = json.loads(response)["results"][0]["formatted_address"]
        return address
    
    def getAddressFromCoordinates(self, lat, long): # returns the street address given cooordinates as arguments
        api_key = "AIzaSyBye-KERYIXDd24hk0C19mSMXdS7TmCX3M"
        coordinates = str(lat) + "," + str(long)
        link = "https://maps.googleapis.com/maps/api/geocode/json?latlng={}&key={}".format(coordinates, api_key)
        response = urllib.request.urlopen(link).read()
        address = json.loads(response)["results"][0]["formatted_address"]
        return address
    
    def getCoordinatesFromAddress(self, address): # performs geocoding to return coordinates given a street address
        api_key = "AIzaSyBye-KERYIXDd24hk0C19mSMXdS7TmCX3M"
        address = address.replace(" ", "+")
        link = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}".format(address, api_key)
        response = urllib.request.urlopen(link).read()
        data = json.loads(response)
        latitude = data["results"][0]["geometry"]["location"]["lat"]
        longitude = data["results"][0]["geometry"]["location"]["lng"]
        return [latitude, longitude]
    
    def distance(self, lat1, lng1, lat2, lng2): # finds the distance between two sets of coordinates
        degtorad = math.pi/180
        dLat = (lat1-lat2)*degtorad
        dLng = (lng1-lng2)*degtorad
        a = pow(math.sin(dLat/2), 2) + math.cos(lat1*degtorad)*math.cos(lat2*degtorad)*pow(math.sin(dLng/2), 2)
        b = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
        return 6371*b
    
    def distanceToHome(self): # finds the distance to the home address that was set
        f = open("home.txt", "r")
        home = f.readlines()[0]
        f.close()
        lat, lng = g.getCoordinatesFromAddress(home)
        g.refresh()
        lat2 = g.getLatitude()
        lng2 = g.getLongitude()
        return self.distance(lat, lng, lat2, lng2)
    
    def setHomeAddress(self, address): # sets home address
        f = open("home.txt", "w")
        f.write(home)
        f.close()
    
    def getHomeAddress(self): # returns home address
        f = open("home.txt", "r")
        a = f.readlines()
        return a[0]
    
    def logLocation(self):
        global refresh
        
        time_start = time.time()
        dt = datetime.datetime.now()
        address1 = self.getCurrentAddress()
        h = open("history.txt", "a")
        h.write(str(dt) + "\n")
        h.write(address1 + "\n")
        h.close()
        while True:
            address2 = self.getCurrentAddress()
            print(address2+"\n")
            if address1 != address2:
                time_elapsed = time.time() - time_start
                print(time_elapsed + "\n")
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
            time.sleep(refresh)
    
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
    gps = location_calcs()
    #gps.logLocation()
#     print(gps.getCoordinatesFromAddress("19 Loots Road Blairgowrie, Randburg"))
#     print(gps.distance(-26.103062, 28.003815, -26.116043, 28.001292))
#     print(gps.locationAtTime("2020-10-14 20:22:14.850905"))
#     print(gps.timesAtLocation("address3"))
