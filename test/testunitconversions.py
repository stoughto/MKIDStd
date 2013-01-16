import unittest
import MKIDStd
import matplotlib.pyplot as plt
import string
import numpy
class TestUnitConversion(unittest.TestCase):

    def testPlot(self):
        std = MKIDStd.MKIDStd()
        #aFinal = std.load('hiltner600')
        aOriginal = numpy.loadtxt('../data/mhilt600.dat')
        plt.clf()
        plt.plot(aOriginal[:,0],aOriginal[:,1])
        plt.show()

    def testMagToErgs(self):
        std = MKIDStd.MKIDStd()
        aOriginal = numpy.loadtxt('../data/mhilt600.dat')
        # insert conversion
        plt.subplot(212)
        plt.plot()
        plt.show()

#    def testMagtoCounts(self):
        std = MKIDStd.MKIDStd()
        aOriginal = numpy.loadtxt('../data/mhilt600.dat')
        # insert conversion
        plt.clf()
        plt.plot()
        plt.show()
        

if __name__ == '__main__':
unittest.main()
