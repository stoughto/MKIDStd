import os
import glob
class MKIDStd:
    """
    This is a useful description of this class
    """

    def __init__(self):
        """
        Loads up the list of objects we know about
        """
        self.junk = "This is junk"
        self.objects = {}
        
        for file in glob.glob("data/*.txt"):

            name,ext = os.path.splitext(os.path.basename(file))
            dictionary = self._loadDictionary(file)
            self.objects[name] = dictionary

    def _loadDictionary(self,file):
        retval = {}
        for line in open(file):
            vals = line.strip().split(" = ");
            retval[vals[0]] = vals[1:]

        return retval
