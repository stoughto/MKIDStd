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
        this_dir, this_filename = os.path.split(__file__)        
        pattern = os.path.join(this_dir,"data","*.txt")
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
