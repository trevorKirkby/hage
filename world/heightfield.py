import sys
import os.path
import array

class Error(Exception):
    def __init__(self,msg):
        self.msg = msg
    def __str__(self):
        return repr(self.msg)
    
"""
A heightfield represents the elevation relative to sea level on a pixelated spherical planet.
"""
class Heightfield:
    """
    Reads a height field from a binary file using 16-bit signed integers for each pixel.
    Raises a heightfield.Error in case of any problems.
    """
    def __init__(self,filename,npixels):
        # create an empty array to hold the heightfield data as unsigned shorts
        self.data = array.array('H')
        try:
            # check that the file has the expected size
            if os.path.getsize(filename) != 2*npixels:
                raise Error('Heightfield file "%s" has wrong size %d (expected %d)' %
                    (filename,os.path.getsize(filename),2*npixels))
            # open the file in binary read-only mode
            with open(filename,"rb") as f:
                try:
                    self.data.fromfile(f,npixels)
                except EOFError:
                    raise Error('Unexpected EOF in heightfield file "%s"' % filename)
        except (IOError,OSError):
            raise Error('Unable to read heightfield file "%s"' % filename)
        # data in file is in network byte order (big endian) so swap here if necessary
        if sys.byteorder == "little":
            self.data.byteswap()

if __name__ == "__main__":
    h = Heightfield("world/data/poodle.hf",4800)
    print "ok"
