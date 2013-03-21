import sys
import array

"""
A heightfield represents the elevation relative to sea level on a pixelated spherical planet.
"""
class Heightfield:
    """
    Reads a height field from a binary file using 16-bit signed integers for each pixel.
    """
    def __init__(self,filename,npixels):
        # create an empty array to hold the heightfield data as unsigned shorts
        self.data = array.array('H')
        # open the file in binary read-only mode
        with open(filename,"rb") as f:
            try:
                self.data.fromfile(f,npixels)
            except EOFError:
                print 'Not enough bytes in heightfield file',filename
        # data in file is in network byte order (big endian) so swap here if necessary
        if sys.byteorder == "little":
            self.data.byteswap()

if __name__ == "__main__":
    h = Heightfield("world/data/poodle.hf",4800)
    print "ok"
