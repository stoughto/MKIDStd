import os
import glob
import matplotlib.pyplot as plt
import numpy
import types
import string
import pyfits
class MKIDStd:
    """
    This is a useful description of this class.  But it could be much better.
    """

    def __init__(self, referenceWavelength=5500):
        """
        Loads up the list of objects we know about
        """
        self.referenceWavelength=referenceWavelength
        self.objects = {}
        self.this_dir, this_filename = os.path.split(__file__)        

        pattern = os.path.join(self.this_dir,"data","*.txt")
        for file in glob.glob(pattern):
            name,ext = os.path.splitext(os.path.basename(file))
            dictionary = self._loadDictionary(file)
            self.objects[name] = dictionary

    def _loadDictionary(self,file):
        retval = {}
        for line in open(file):
            vals = line.strip().split(" = ");
            retval[vals[0]] = vals[1:]
        return retval

    def load(self,name):
        """
        Returns a two dimensional numpy array where a[:,0] is wavelength in
        Angstroms and a[:,1] is flux in counts/sec/angstrom/cm^2
        """
        fname = self.objects[name]['dataFile']
        fullFileName = os.path.join(self.this_dir,"data",fname[0])
        a = numpy.loadtxt(fullFileName)
        referenceFlux = self.getFluxAtReferenceWavelength(a)
        ergs = string.count(self.objects[name]['fluxUnit'],"ergs")
        if ergs:
            a[:,1]/= a[:,0]
            print "converting from ergs"
        mag = string.count(self.objects[name]['fluxUnit'],"mag")
        if mag:
            a[:,1] = 10**(-.04*a[:,1])
            print "converting from mag"
        a[:,1] /= referenceFlux
        return a

    def plot(self,name="all",xlog=False,ylog=True,xlim=[3000,10000]):
        if (name == "all"):
            listofobjects = self.objects.keys()
            plotname = "all"
        elif (isinstance(name, types.ListType)):
            listofobjects = name
            plotname = name[0]+"_group"
        else:
            plotname = name
            listofobjects = [name]
        plt.clf()
        plotYMin = 1
        plotYMax = 1
        for tname in listofobjects:
            print "tname=", tname
            a = self.load(tname)
            a.shape
            x = a[:,0]
            y = a[:,1]
            if (not xlog and ylog):
                plt.semilogy(x,y, label=tname)
            if (not ylog and xlog):
                plt.semilogx(x,y, label=tname)
            if (not xlog and not ylog):
                plt.plot(x,y, label=tname)
            if (xlog and ylog):
                plt.loglog(x,y, label=tname)
            imin = numpy.searchsorted(x,xlim[0])
            imax = numpy.searchsorted(x,xlim[1])
            ytemp = y[imin:imax]
            ymin = ytemp.min()
            ymax = ytemp.max()
            plotYMin = min(plotYMin,ymin)
            plotYMax = max(plotYMax,ymax)
       
        plt.xlabel('wavelength(Angstroms)')
        plt.ylabel('flux(counts/sec/angstrom/cm^2)')
        plt.legend()
        plt.xlim(xlim)
        plt.ylim([plotYMin,plotYMax])
        print "plotname=", plotname
        plt.savefig(plotname+'.png')
	
    def getFluxAtReferenceWavelength(self, a):
        x = a[:,0]
        y = a[:,1]
	index = numpy.searchsorted(x, self.referenceWavelength);
	return y[index]

    def ShowUnits(self):

        for name in self.objects.keys():
            fluxUnit = self.objects[name]['fluxUnit']
            print name, " ", fluxUnit

    def loadSdssSpecFits(self, fullFileName):
        f = pyfits.open(fullFileName)
        coeff0 = f[0].header['COEFF0']
        coeff1 = f[0].header['COEFF1']
        n = len(f[1].data)
        retval = numpy.zeros([n,2])
        retval[:,0] = numpy.arange(n)
        retval[:,0] = 10**(coeff0+coeff1*retval[:,0])
        for i in range(n):
            retval[i][1] = f[1].data[i][0]
        return retval
