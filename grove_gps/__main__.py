from grove_gps import GPS

def main():
    g = GPS()
    print("Latitude:", g.getLatitude())
    print("Longitude:", g.getLongitude())
    print("Altitude:", g.getAltitude())
    print("Number of satellites:", g.getSatellites())

if __name__ == "__main__":
    main()