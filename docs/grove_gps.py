#The GPS module used is a Grove GPS module http://www.seeedstudio.com/depot/Grove-GPS-p-959.html

import serial, time
    
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
    inp = []
    inp2 = []
    GGA = []
    RMC = []
    values = []
    
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
    