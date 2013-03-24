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
