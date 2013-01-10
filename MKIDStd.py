import os
import glob
import matplotlib.pyplot as plt
import numpy
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
        a[:,1] /= referenceFlux
        return a

    def plot(self,name="all"):
        if (name == "all"):
            for tname in self.objects.keys():
                print "tname=", tname
                a = self.load(tname)
                a.shape
                x = a[:,0]
                y = a[:,1]
                plt.loglog(x,y, label=tname)
        else:
            a = self.load(name)
            x = a[:,0]
            y = a[:,1]
            plt.loglog(x,y, label=name)
       	
	plt.xlabel('wavelength(Angstroms)')
        plt.ylabel('flux(counts/sec/angstrom/cm^2)')
        plt.legend()
        plt.savefig(name+'.png')
	
    def getFluxAtReferenceWavelength(self, a):
        x = a[:,0]
        y = a[:,1]
	index = numpy.searchsorted(x, self.referenceWavelength);
	return y[index]