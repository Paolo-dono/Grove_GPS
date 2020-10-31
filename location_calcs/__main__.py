from location_calcs import location_calcs

def main():
    gps = location_calcs()
    print("Distance between [-26.103062, 28.003815] and [-26.116043, 28.001292]:",
          gps.distance(-26.103062, 28.003815, -26.116043, 28.001292))
    
if __name__ == "__main__":
    main()
