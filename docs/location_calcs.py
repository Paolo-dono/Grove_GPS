from grove_gps import GPS
import time
import datetime
import json
import math
import urllib.request
import sys

class location_calcs:
    """Perform calculations on values fetched from GPS"""
    g = None
    refresh = 30
    api_key = ""
    
    def __init__(self):
        """Instantiate an object of the class and initialises the
        global variables
        """
        global g
        global refresh
        global api_key
        
        g = GPS()
        refresh = 30
        api_key = ""
        try:
            f = open("api_key.txt", "r")
            api_key = f.readlines()[0]
            f.close()
        except FileNotFoundError:
            print("No API key found")
    
    def getLogRefreshRate(self):
        """Return the rate at which new locations are added to the 
        history log of locations visited
        """
        #global refresh
        return refresh
    
    def setLogRefreshRate(self, new_refresh):
        """Set a new refresh rate for the history log"""
        global refresh
        refresh = new_refresh
    
    def setAPIkey(self, key):
        """Set API key and store it in a text file"""
        global api_key
        
        f = open("api_key.txt", "w")
        f.write(key)
        f.close()
        api_key = key
    
    def getAPIkey(self):
        """Return API keyfrom text file"""
        try:
            f = open("api_key.txt", "r")
            a = f.readlines()
            return a[0]
        except FileNotFoundError:
            print("No API key found")
    
    def getCurrentAddress(self):
        """Perform reverse geocoding to return the current street
        address from the coordinates read from the GPS module
        """
        global g
        global api_key
        
        g.refresh() # fetches new values from the GPS
        coordinates = str(g.getLatitude()) + "," + str(g.getLongitude())
        link = "https://maps.googleapis.com/maps/api/geocode/json?" + \
            "latlng={}&key={}".format(coordinates, api_key)
        
        # fetches data from the Google Maps API
        response = urllib.request.urlopen(link).read()
        data = json.loads(response)
        
        # finds address from the data
        address = data["results"][0]["formatted_address"]
        return address
    
    def getAddressFromCoordinates(self, lat, long):
        """Return the street address given cooordinates
        as arguments
        """
        global api_key
        
        coordinates = str(lat) + "," + str(long)
        link = "https://maps.googleapis.com/maps/api/geocode/json?" + \
            "latlng={}&key={}".format(coordinates, api_key)
        
        # fetches data from the Google Maps API
        response = urllib.request.urlopen(link).read()
        data = json.loads(response)
        
        # finds address from the data
        address = data["results"][0]["formatted_address"]
        return address
    
    def getCoordinatesFromAddress(self, address):
        """Perform geocoding to return coordinates
        given a street address
        """
        global api_key
        
        address = address.replace(" ", "+")
        link = "https://maps.googleapis.com/maps/api/geocode/json?" + \
            "address={}&key={}".format(address, api_key)
        
        # fetches data from the Google Maps API
        response = urllib.request.urlopen(link).read()
        data = json.loads(response)
        
        # finds coordinates from data
        latitude = data["results"][0]["geometry"]["location"]["lat"]
        longitude = data["results"][0]["geometry"]["location"]["lng"]
        return [latitude, longitude]
    
    def distance(self, lat1, lng1, lat2, lng2):
        """Find the distance between two sets of coordinates"""
        degtorad = math.pi / 180
        dLat = (lat1-lat2) * degtorad
        dLng = (lng1-lng2) * degtorad
        a = pow(math.sin(dLat/2), 2) + math.cos(lat1*degtorad) * \
            math.cos(lat2*degtorad) * pow(math.sin(dLng/2), 2)
        b = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
        return 6371*b
    
    def distanceToHome(self):
        """Find the distance to the home address that was set"""
        f = open("home.txt", "r")
        home = f.readlines()[0]
        f.close()
        lat, lng = g.getCoordinatesFromAddress(home)
        g.refresh()
        lat2 = g.getLatitude()
        lng2 = g.getLongitude()
        return self.distance(lat, lng, lat2, lng2)
    
    def setHomeAddress(self, address):
        """Set home address and store it in a text file"""
        f = open("home.txt", "w")
        f.write(address)
        f.close()
    
    def getHomeAddress(self):
        """Return home address from text file"""
        try:
            f = open("home.txt", "r")
            a = f.readlines()
            return a[0]
        except FileNotFoundError:
            print("No address found")
    
    def logLocation(self):
        """Build history of locations visited"""
        global refresh
        
        # this block creates a new entry in the history log
        # with the current location and timestamp
        # because it is assumed the GPS was turned off for some time
        # so it has to start a new log 
        time_start = time.time()               
        dt = datetime.datetime.now()           
        address1 = self.getCurrentAddress()
        h = open("history.txt", "a")
        h.write(str(dt) + "\n")
        h.write(address1 + "\n")
        h.close()
        
        while True: # infinite loop for continuous logging
            address2 = self.getCurrentAddress()
            if address2 != address1: # check if location has changed
                time_elapsed = time.time() - time_start
                # if at least 10 minutes has passed,
                # address1 is seen as a visit and so
                # address1 had to be updated in the favourites file
                if time_elapsed > 600: 
                    favourites = open("favourites.txt") 
                    fav = json.load(favourites)
                    favourites.close()
                    # if address1 is already in the favourites file,
                    # the number of visitations is incremented
                    # otherwise it is added to the file
                    # with an initial value
                    if address1 in fav:   
                        fav[address1] += 1 
                    else:
                        fav[address1] = 1 
                    new_favourites = open("favourites.txt", "w")
                    json.dump(fav, new_favourites)
                    new_favourites.close()
                
                # add a log to the history file
                dt = datetime.datetime.now()
                f = open("history.txt", "a")
                f.write(str(dt) + "\n")
                f.write(address2 + "\n")
                f.close()
                
                # the reference address (address1)
                # is changed to address2
                address1 = address2
                time_start = time.time()   # sets a new start time
            time.sleep(refresh) # rate at which logging takes place
    
    def getFavouriteLocations(self):
        """Return a list of top 5 favourite locations"""
        # reads in dictionary of all visited locations
        # note: a visit is seen as remaining at the same location
        # for at least 10 minutes
        favourites = open("favourites.txt")
        fav = json.load(favourites)
        favourites.close()
        top = [] # stores a list of most visited places
        
        for i in range(5):
            highest = 0 # stores highest number of visits
            place = "" # stores address of that location
            # this loop finds the highest number of visits
            # in the dictionary
            for j in fav: 
                if fav[j] > highest:
                    highest = fav[j]
                    place = j
            
            # the most visited location is removed
            # and added to the list of most visited places
            fav.pop(place)
            top.append(place) 
        return top
    
    def locationAtTime(self, dt):
        """Return the location of the gps at a given time"""
        f = open("history.txt", "r")
        data = f.readlines() # read all history logs
        f.close()
        start = 0
        stop = len(data)
        found = False
        address = ""
        # search through the data using an interval search algorithm
        while found == False:
            pos = (stop-start)//2 + start
            if pos%2 == 1:
                pos -= 1
            if dt < data[pos][:19]:
                stop = pos
            else:
                start = pos
            if (stop - start) == 2:
                found = True
                address = data[start+1]
        return address
    
    def timesAtLocation(self, address):
        """Return the number of times a given address was visited"""
        favourites = open("favourites.txt")
        fav = json.load(favourites)
        favourites.close()
        return fav[address]

if __name__ == "__main__":
    gps = location_calcs()
    print("Current address:", gps.getCurrentAddress())
    print("Coordinates:",
          gps.getCoordinatesFromAddress("46 6th Street, Linden, Randburg"))
    print("Distance:", gps.distance(-26.103062, 28.003815,
                                    -26.116043, 28.001292))
    print("Address:", gps.getAddressFromCoordinates(-26.103062, 28.003815))
    print("Location at 2020-10-21 18:27:27 :",
          gps.locationAtTime("2020-10-21 18:27:27"))
