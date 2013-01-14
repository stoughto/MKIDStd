import unittest
import numpy as np
import MKIDStd
import matplotlib.pyplot as plt
import smooth
class TestSmooth(unittest.TestCase):

    def testSmoothDelta(self):
        nIn = 100;
    
        x = np.zeros(nIn)
        x[nIn/2] = 1

        len = 21
        xs = smooth.smooth(x, window_len=len)
        plt.clf()
        plt.plot(x)
        plt.plot(xs[len/2:-(len/2)])
        plt.savefit("testSmoothDelta.png")

    def testSmoothZCosmos(self):
        std = MKIDStd.MKIDStd()
        raw = std.load("zcosmos841948")
        plt.plot(raw[:,0],raw[:,1], label="raw")

        len = 31
        smoothed = smooth.smooth(raw[:,1],window_len=len)
        plt.plot(raw[:,0],smoothed[len/2:-(len/2)], label="smoothed")

        plt.legend()
        plt.show()

if __name__ == '__main__':
    unittest.main()
