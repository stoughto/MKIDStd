import os
import glob
import matplotlib.pyplot as plt
import numpy
import types
import string
import pyfits
import smooth
import sys
from scipy.constants import *

class MKIDStd:
    """
    This class contains the spectra of several standard stars. These
    spectra may be plotted and used to compare with data from the MKID
    detector.

    Wavelength and flux values  and text files describing each object are saved in
    data.
    """

    def __init__(self, referenceWavelength=6500):
        """
        Loads up the list of objects we know about
        The reference wavelength is set at 6500 if _init_()
        """
        self.referenceWavelength=referenceWavelength
        self.objects = {}
        self.filters = {}
        self.filterList = ['U','B','V','R','I','g','i','r','u','z']
        self.this_dir, this_filename = os.path.split(__file__)        

        pattern = os.path.join(self.this_dir,"data","*.txt")
        for file in glob.glob(pattern):
            name,ext = os.path.splitext(os.path.basename(file))
            dictionary = self._loadDictionary(file)
            self.objects[name] = dictionary
        self.balmerwavelengths = [6563,4861,4341,4102,3970,3889,3835,3646]
        self.lymanwavelengths = [1216,1026,973,950,938,931,926,923,921,919]

        self._loadFilterFile()
        self._loadfilters()
        self.k = (1*10**-10/1*10**7)/h/c
        """
        h is in Joules/sec and c is in meters/sec. This k value is used in all unit conversions
        """


    def _loadFilterFile(self):
            
        filterFileName = os.path.join(self.this_dir,"data","ph08_UBVRI.mht")
        f = open(filterFileName,'r')
        nFilter = -1
        nToRead = -1
        iFilter = -1
        iRead = 0
        for line in f:
            if (nFilter == -1) :
                nFilter = int(line)
            elif (nToRead <= 0):
                nToRead = int(line)
                iFilter += 1
                filter = self.filterList[iFilter]
                self.filters[filter] = numpy.zeros((2,nToRead))
                iRead = 0
            else:
                nToRead -= 1
                vals = line.split()
                self.filters[filter][0,iRead] = vals[0]
                self.filters[filter][1,iRead] = vals[1]
                iRead += 1    

    def _loadfilters(self):
        for filter in ['u','g','i','r','z']:
            filterFileName = os.path.join(self.this_dir,"data",filter+'.mht')
            numpy.loadtxt(filterFileName)
            self.filters[filter] = numpy.zeros((1,4))
            

    def _loadDictionary(self,file):
        retval = {}
        for line in open(file):
            vals = line.strip().split(" = ");
            retval[vals[0]] = vals[1:]
        return retval

    def load(self,name):
        """
        Returns a two dimensional numpy array where a[:,0] is
        wavelength in
        Angstroms and a[:,1] is flux in counts/sec/angstrom/cm^2
        
        Plots containing a lot of noise are smoothed.
        """
        fname = self.objects[name]['dataFile']
        fullFileName = os.path.join(self.this_dir,"data",fname[0])
        if (string.count(fullFileName,"fit")):
            a = self.loadSdssSpecFits(fullFileName)
        else:
            a = numpy.loadtxt(fullFileName)

        len = int(self.objects[name]['window_len'][0])
        if len > 1:
            a[:,1] = smooth.smooth(a[:,1], window_len=len)[len/2:-(len/2)]
            
        ergs = string.count(self.objects[name]['fluxUnit'][0],"ergs")
        if ergs:
            a[:,1] *= (a[:,0] * self.k)
        mag = string.count(self.objects[name]['fluxUnit'][0],"mag")
        if mag:
            a[:,1] = (10**(-2.406/2.5))*(10**(-0.4*a[:,1]))/(a[:,0]**2) * (a[:,0] * self.k)
        return a

    def normalizeFlux(self,a):
        referenceFlux = self.getFluxAtReferenceWavelength(a)
        a[:,1] /= referenceFlux
        return a

    def countsToErgs(self,a):
        a[:,1] /= (a[:,0] * self.k)
        return a
    
    def measureBandPassFlux(self,aFlux,aFilter):
        sum = 0
        sumd = 0
        filter = numpy.interp(aFlux[:,0], aFilter[0,:], aFilter[1,:], 0, 0)
        for i in range(aFlux[:,0].size-1):
            dw = aFlux[i+1,0] - aFlux[i,0]
            flux = aFlux[i,1]*filter[i]/aFlux[i,0]
            sum += flux*dw
            sumd += filter[i]*dw
            sum /= self.k
            sum /= sumd
        return sum

    def plot(self,name="all",xlog=False,ylog=True,xlim=[3000,10000],normalizeFlux=True,countsToErgs=False):
        """
        Returns a graph that plots the arrays a[:,0] (wavelength) and
        a[:,1] (flux) with balmer wavelengths indicated. Individual
        spectra are labeled and indicated by a legend.
        plot() plots the spectrum of all standard stars in the program.
        plot(['vega'],['bd17']) returns only the spectrum for those two
        stars.
        plot('vega') returns the spectrum for only that star.
        The y array for each plot is presented as a logarithm, while the 
        x array is linear if plot()
        x limits are set between 3,000 and 10,000 and y limits are calculated based
        on those values.
        Plots are saved as plotname.png
        """
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
        plotYMin = -1
        plotYMax = -1
        for tname in listofobjects:
            print "tname=", tname
            a = self.load(tname)
            if (countsToErgs):
                a = self.countsToErgs(a)
            if (normalizeFlux):
                a = self.normalizeFlux(a)
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
            ymin = abs(ytemp).min()
            ymax = ytemp.max()
            if (plotYMin == -1):
                plotYMin = ymin
                plotYMax = ymax
            else:
                plotYMin = min(plotYMin,ymin)
                plotYMax = max(plotYMax,ymax)
            print "ymax=",ymax, "plotYMax=",plotYMax
        
        for x in self.balmerwavelengths:
            plt.plot([x,x],[plotYMin,plotYMax], 'r--')
       
        plt.xlabel('wavelength(Angstroms)')
        
        if (countsToErgs):
            ylabel = 'flux(ergs/sec/cm2/A)'
        else:
            ylabel = 'flux(counts/sec/cm2/A)'

        if (normalizeFlux):
            ylabel += '['+str(self.referenceWavelength)+']'

        plt.ylabel(ylabel)
        ax = plt.subplot(111)
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax.legend(bbox_to_anchor=(1.05,1), loc=2, prop={'size':10}, borderaxespad=0.)
        plt.xlim(xlim)
        print "set ylim with plotYMin=",plotYMin,"  plotYMax=",plotYMax
        plt.ylim([plotYMin,plotYMax])
        print "plotname=", plotname
        plt.savefig(plotname+'.png')
	

    def plotfilters(self):
        plt.clf()
        listoffilters = self.filterList
        for filter in listoffilters:
            a = self.filters[filter]
            y = a[1,:]
            x = a[0,:]
            plt.plot(x,y, label=filter)
            plt.legend()
            plt.savefig('filters'+'.png')
        

    def getFluxAtReferenceWavelength(self, a):
        """
        returns the flux value corresponding with the reference
        wavelength (6500).
        """
        x = a[:,0]
        y = a[:,1]
	index = numpy.searchsorted(x, self.referenceWavelength);
        if index < 0:
            index = 0
        if index > x.size - 1:
            index = x.size - 1
            print "index=", index
	return y[index]

    def ShowUnits(self):
        """
        Returns flux units for the spectra of objects.
        """

        for name in self.objects.keys():
            fluxUnit = self.objects[name]['fluxUnit']
            print name, " ", fluxUnit

    def loadSdssSpecFits(self, fullFileName):
        """
        Allows spectral data from  a fits file to be read into the program
        """
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

    def report(self, xlim=[500,10000000]):
        """
        Creates a text document that reports the units, citation, and
        description of each object
        """
	old_stdout = sys.stdout
	log_file = open("Report.log","w")
	sys.stdout = log_file
	for name in self.objects.keys():
	    fluxUnit = self.objects[name]['fluxUnit'][0]
	    wavelengthUnit = self.objects[name]['wavlengthUnit'][0]
	    citation = self.objects[name]['citation'][0]
	    description = self.objects[name]['description'][0]
	    a = self.load(name)
            a.shape
	    points = a[:,1].size
            x = a[:,0]
            y = a[:,1]
	    imin = numpy.searchsorted(x,xlim[0])
            imax = numpy.searchsorted(x,xlim[1])
            xtemp = x[imin:imax]
            xmin = abs(xtemp).min()
            xmax = xtemp.max()
	    WavelengthMin = xmin
	    WavelengthMax = xmax
	    print "---------------------------------------------------------------------------------------"
	    print "Name: %s" %name
	    print "Units: Flux: %s Wavelength: %s " %(fluxUnit, wavelengthUnit) 
	    print "Citation: %s" %citation
	    print "Description: %s." %description
	    print "Number of Points: %d Wavelength: Max =%9.3f Min = %10.3f" %(points, WavelengthMin, WavelengthMax)
	    
	sys.stdout = old_stdout
	log_file.close()
