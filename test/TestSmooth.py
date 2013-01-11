import unittest
import numpy as np
import MKIDStd
import matplotlib.pyplot as plt
import smooth
class TestSmooth(unittest.TestCase):

    def testSmooth(self):
        std = MKIDStd.MKIDStd()
        raw = std.load("zcosmos841948")
        plt.plot(raw[:,0],raw[:,1], label="raw")

        smoothed = smooth.smooth(raw[:,1],window_len=21)
        plt.plot(raw[:,0],smoothed[:len(raw)], label="smoothed")

        plt.legend()
        plt.show()

if __name__ == '__main__':
    unittest.main()
