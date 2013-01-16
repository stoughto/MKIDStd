import unittest
import MKIDStd
import matplotlib.pyplot as plt
import numpy
import math
from scipy.constants import *
class TestUnitConversion(unittest.TestCase):

    def testPlot(self):
        std = MKIDStd.MKIDStd()
        #aFinal = std.load('hiltner600')
        aOriginal = numpy.loadtxt('../data/mhilt600.dat')
        plt.clf()
        plt.subplot(211)
        plt.plot(aOriginal[:,0],aOriginal[:,1], label='ABmag')
        plt.gca().invert_yaxis()
        plt.legend()
        f = (10**(-2.406/2.5))*(10**(-0.4*aOriginal[:,1]))/(aOriginal[:,0]**2)  
        plt.subplot(212)
        plt.plot(aOriginal[:,0],f, label='ergs')
        plt.legend()
        plt.show()
      
    def testMagtoCounts(self):
        std = MKIDStd.MKIDStd()
        aOriginal = numpy.loadtxt('../data/mhilt600.dat')
        f = (10**(-2.406/2.5))*(10**(-0.4*aOriginal[:,1]))/(aOriginal[:,0]**2)
        fcounts = f * aOriginal[:,0] * 5.03*10**7
        plt.figure(2)
        plt.plot(aOriginal[:,0],fcounts, label='counts')
        plt.legend()
        plt.show()
        

if __name__ == '__main__':
    unittest.main()
