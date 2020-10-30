import os
from grove_gps import GPS

g = GPS()
broker = "test.mosquitto.org"
port = "1883"
topic = "gps-1"

try:
    while True:
        os.system("mosquitto_pub -h \"" + broker + "\" -p " + port + " -t " + topic + " -m \"" + str(g.getLatitude()) + "," + str(g.getLongitude()) + "\"")
        print("mosquitto_pub -h \"" + broker + "\" -p " + port + " -t " + topic + " -m \"" + str(g.getLatitude()) + "," + str(g.getLongitude()) + "\"")
        g.refresh()
except KeyboardInterrupt:
    print("End")
        
        
        