import math

class Error(Exception):
    def __init__(self,msg):
        self.msg = msg
    def __str__(self):
        return repr(self.msg)

"""
HEALPix is a method of subdividing a sphere into equal area pixels. See http://healpix.jpl.nasa.gov
for details.
"""
class HEALPixMap:
    """
    Creates the mapping between pixels and position on the sphere for the specified grid size
    parameter nsides.
    """
    def __init__(self,nsides):
        if nsides < 1:
            raise Error('Invalid nsides < 1 in HEALPixMap')
        self.nsides = nsides
        self.npixels = 12*nsides*nsides
        self.ncap = 2*nsides*(nsides-1)
    """
    Tests if the specified pixel index is valid
    """
    def isValidPixel(self,pixel):
        return pixel >= 0 and pixel < self.npixels
    """
    Returns the (i,j,z,phi) tuple for the specified pixel center
    """
    def getPixel(self,pixel):
        if not self.isValidPixel(pixel):
            raise Error('Invalid pixel index %d in getLatLon' % pixel)
        if pixel < self.ncap:
            # pixel is in north polar cap
            i = int(math.floor(0.5*(1+math.floor(math.sqrt(2*pixel+1.5)))))
            j = pixel+1-2*i*(i-1)
            z = 1.0-i*i/(3.*self.nsides*self.nsides)
            phi = math.pi/(2*i)*(j-0.5)
        elif pixel < self.npixels - self.ncap:
            # pixel is in the equatorial belt
            ph = pixel-self.ncap
            i = int(math.floor(ph/(4.0*self.nsides))+self.nsides)
            j = ph%(4*self.nsides)+1
            z = 2.0*(2*self.nsides-i)/(3.0*self.nsides)
            if (i+self.nsides)%2 == 1:
                s = 1.0
            else:
                s = 0.5
            phi = math.pi/(2*self.nsides)*(j-s)
        else:
            # pixel is in the south polar cap
            ph = self.npixels-pixel
            i = int(math.floor(0.5*(1+math.floor(math.sqrt(2*ph-0.5)))))
            j = 4*i+1-(ph-2*i*(i-1))
            z = -1+i*i/(3.0*self.nsides*self.nsides)
            phi = math.pi/(2*i)*(j-0.5)
        return (i,j,z,phi)