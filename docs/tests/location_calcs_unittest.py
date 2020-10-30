from location_calcs import location_calcs
import unittest

class test_location_calcs(unittest.TestCase):
    
    def test_getCoordinatsFromAddress(self):
        g = location_calcs()
        print(g.setHomeAddress.__doc__)
        self.assertEqual(
            g.getCoordinatesFromAddress("46 6th Street, Linden, Randburg"),
            [-26.13819, 27.99231])
    
    def test_distance(self):
        g = location_calcs()
        self.assertEqual(
            g.distance(-26.103062, 28.003815, -26.116043, 28.001292),
            1.4652395837201548)
    
    def test_getAddressFromCoordinates(self):
        g = location_calcs()
        self.assertEqual(
            g.getAddressFromCoordinates(-26.103062, 28.003815),
            "168 Barkston Dr, Blairgowrie, Randburg, 2194, South Africa")
    
    def test_home(self):
        g = location_calcs()
        g.setHomeAddress("7 Orpen Street, Secunda")
        self.assertEqual(g.getHomeAddress(), "7 Orpen Street, Secunda")
    
    def test_refresh(self):
        g = location_calcs()
        g.setLogRefreshRate(10)
        self.assertEqual(g.getLogRefreshRate(), 10)

if __name__ == "__main__":
    unittest.main()
