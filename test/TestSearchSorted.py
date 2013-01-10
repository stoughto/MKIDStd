import unittest
import numpy as np
class TestTimeMask(unittest.TestCase):

    def testGetIndex(self):
        w = 3000+2*np.arange(1000)
        referenceWavelength = 4567.89
        index = np.searchsorted(w, referenceWavelength);
        print "w[index-1]=",w[index-1]
        print "referenceWavelength=",referenceWavelength
        print "w[index]=",w[index]

if __name__ == '__main__':
    unittest.main()
