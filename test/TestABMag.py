import unittest
import numpy as np
import math
class TestAB(unittest.TestCase):

    def testConvert(self):
        """
        Test the equation for converting AB magnitude to flux and back again, 
        from http://en.wikipedia.org/wiki/AB_magnitude
        """
        for i in range(100):
            AB = 10 + i/10.0
            wave = 1000 + 100*i
            f = (10**(-2.406/2.5))*(10**(-0.4*AB))/(wave**2)
            AB_new = -2.5*math.log10(f) - 5*math.log10(wave) - 2.406
            #print "AB=",AB,"  wave=",wave, " f=",f, "  AB_new=",AB_new
            self.assertAlmostEqual\
                (AB, AB_new, msg="AB=%f f=%f AB_new=%f" % (AB, f, AB_new))
if __name__ == '__main__':
    unittest.main()
