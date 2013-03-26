import sys
import os.path
import array

import healpix

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
    Raises an Error in case of any problems.
    """
    def __init__(self,filename,nside):
        try:
            self.pixmap = healpix.HEALPixMap(nside)
            npixels = self.pixmap.npixels
        except healpix.Error:
            raise Error('Invalid nside < 1 for heightfield.')
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
        # precompute the conversion from internal (16-bit unsigned) to external (normalized
        # floating point), i.e., the float constant 2^-16
        self.conversion = float(1.52587890625e-5)
    """
    Returns the height relative to sea level or raises an Error for an invalid pixel.
    """
    def getHeight(self,pixel):
        if not self.pixmap.isValidPixel(pixel):
            raise Error('Invalid pixel index %d in Heightfield.getHeight.' % pixel)
        return self.conversion*self.data[pixel]
