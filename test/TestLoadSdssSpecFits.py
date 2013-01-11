import unittest
import MKIDStd
class TestSdssFits(unittest.TestCase):

    def testLoad(self):
        std = MKIDStd.MKIDStd()
        std.loadSdssSpecFits("../data/spec-2694-54199-0528.fits")

if __name__ == '__main__':
    unittest.main()
