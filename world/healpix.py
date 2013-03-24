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
        # Total number of pixels in the map
        self.npixels = 12*nsides*nsides
        # Number of pixels in each polar cap that have special geometry
        self.ncap = 2*nsides*(nsides-1)
        # Number of pixels equally spaced in azimuth for each ring.
        # Note that (i,j) are both indexed starting from 1, following HEALPix conventions.
        self.nrings = 4*nsides-1
        self.nphi = [ 0 ]
        self.nphisum = [ 0 ]
        for i in range(1,self.nrings+1):
            if i < self.nsides:
                n = 4*i
            elif i <= 3*nsides:
                n = 4*self.nsides
            else:
                n = 4*(4*self.nsides-i)
            self.nphisum.append(self.nphisum[-1]+self.nphi[-1])
            self.nphi.append(n)
    """
    Tests if the specified pixel index is valid
    """
    def isValidPixel(self,pixel):
        return pixel >= 0 and pixel < self.npixels
    """
    Returns the (i,j,z,phi) tuple for the specified pixel center
    """
    def getCoordsForPixel(self,pixel):
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
            i = 4*self.nsides - i
        return (i,j,z,phi)
    """
    Returns the pixel index for the specified ring and azimuth indices (i,j).
    Raises an Error for an invalid I but J is wrapped around so is always valid.
    """
    def getPixelForIJ(self,i,j):
        if i < 1 or i > self.nrings:
            raise Error('Invalid ring index %d in getPixelForIJ' % i)
        return self.nphisum[i] + (j-1)%self.nphi[i]
    """
    Returns a triangular mesh that covers the entire sphere
    """
    def getMesh(self):
        mesh = [ ]
        # polar caps
        for iN in range(1,self.nsides):
            iS = 4*self.nsides-iN
            # square pole caps
            if iN == 1:
                mesh.append((iN,1,iN,2,iN,3))
                mesh.append((iN,1,iN,3,iN,4))
                mesh.append((iS,1,iS,2,iS,3))
                mesh.append((iS,1,iS,3,iS,4))
            for g in range(4):
                for j in range(1,iN+1):
                    j1 = iN*g+j
                    j2 = j1+g # (iN+1)*g+j
                    j3 = j2+1  # (iN+1)*g+j+1
                    # polar cap triangles pointing towards the pole
                    mesh.append((iN,j1,iN+1,j2,iN+1,j3))
                    mesh.append((iS,j1,iS-1,j2,iS-1,j3))
                    # polar cap triangles point towards the equator
                    if j < iN:
                        mesh.append((iN,j1,iN,j2+1,iN+1,j3))
                        mesh.append((iS,j1,iS,j2+1,iS-1,j3))
                    # triangles filling in the rectangular holes in the polar caps
                    if j == 1:
                        # j1 = iN*g+1, j2 = (iN+1)*g+1, j3 = (iN+1)*g+2
                        mesh.append((iN,j1,iN,j1-1,iN+1,j2-1))
                        mesh.append((iS,j1,iS,j1-1,iS-1,j2-1))
                        mesh.append((iN,j1,iN+1,j2,iN+1,j2-1))
                        mesh.append((iS,j1,iS-1,j2,iS-1,j2-1))
        # equatorial belt
        for i in range(self.nsides,3*self.nsides):
            for j in range(1,4*self.nsides+1):
                dj = 1-(i+self.nsides)%2;
                mesh.append((i,j,i,j+1,i+1,j+dj))
                mesh.append((i,j+1,i+1,j+dj,i+1,j+dj+1))
        return mesh
    """
    Run self-consitency checks
    """
    def selfTest(self):
        for pixel in range(self.npixels):
            (i,j,z,phi) = self.getCoordsForPixel(pixel)
            pixel2 = self.getPixelForIJ(i,j)
            assert(pixel == pixel2)