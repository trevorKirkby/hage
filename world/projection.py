import math

"""
Projects spherical (phi,z) = (lon,sin(lat)) coordinates, with phi in radians, into (dphi,dz)
coordinates relative to a projection center (phi0,z0). The result can be used directly as
Cartesian coordinates of a Lambert cylindrical equal-area projection.
"""
class Projector:
    def __init__(self,phi0,z0):
        self.z0 = z0
        self.ct0 = math.sqrt(1-z0*z0)
        self.cp0 = math.cos(phi0)
        self.sp0 = math.sin(phi0)
        self.cp0ct0 = self.cp0*self.ct0
        self.sp0ct0 = self.sp0*self.ct0
        self.cp0z0 = self.cp0*self.z0
        self.sp0z0 = self.sp0*self.z0
    """
    Performs the forward projection where phi=lon is in radians and z = sin(lat)
    and returns (dphi,dz) with dphi in radians.
    """
    def project(self,phi,z):
        st = math.sqrt(1-z*z)
        cp = math.cos(phi)
        sp = math.sin(phi)
        dx = self.cp0ct0*cp*st + self.sp0ct0*sp*st + self.z0*z
        dy = self.cp0*sp*st - self.sp0*cp*st
        dz = self.ct0*z - self.cp0z0*st*cp - self.sp0z0*sp*st
        return (math.atan2(dy,dx),dz)
    """
    Performs the inverse projection where dphi is in radians and returns the
    absolute phi in the range (-pi,+pi) and z in the range (-1,+1)
    """
    def unproject(self,dphi,dz):
        st = math.sqrt(1-dz*dz)
        cp = math.cos(dphi)
        sp = math.sin(dphi)
        x = self.cp0ct0*cp*st - self.sp0*sp*st - self.cp0z0*dz
        y = self.cp0*sp*st + self.sp0ct0*cp*st - self.sp0z0*dz
        z = self.ct0*dz + self.z0*cp*st
        return (math.atan2(y,x),z)

class ProjectedMap:
    def __init__(self,left,top,width,height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.right = left + width
        self.bottom = top + height
        self.xcenter = left + 0.5*width
        self.ycenter = top + 0.5*height
        self.setAbsoluteCenter(0,0)
        self.setAbsoluteScale(10)
    def setAbsoluteCenter(self,phi0,z0):
        self.phi0 = phi0
        self.z0 = z0
        self.projector = Projector(phi0,z0)
    def setAbsoluteScale(self,scale):
        self.scale = scale
        self.scaleFactor = 0.5*scale*self.height
    def project(self,phi,z):
        (dphi,dz) = self.projector.project(phi,z)
        x = self.xcenter + self.scaleFactor*dphi
        y = self.ycenter - self.scaleFactor*dz
        return (x,y)
    def contains(self,x,y):
        return x >= self.left and x < self.right and y >= self.top and y < self.bottom
    def render(self,hf):
        # precompute the positions of all vertices
        cache = [ ]
        for pixel in range(hf.pixmap.npixels):
            (i,j,z,phi) = hf.pixmap.getCoordsForPixel(pixel)
            (x,y) = self.project(phi,z)
            cache.append((x,y,hf.getHeight(pixel),self.contains(x,y)))
        # loop over mesh triangles
        for (i1,j1,i2,j2,i3,j3) in hf.pixmap.getMesh():
            p1 = hf.pixmap.getPixelForIJ(i1,j1)
            p2 = hf.pixmap.getPixelForIJ(i2,j2)
            p3 = hf.pixmap.getPixelForIJ(i3,j3)
            (i,j,z1,phi1) = hf.pixmap.getCoordsForPixel(p1)
            (i,j,z2,phi2) = hf.pixmap.getCoordsForPixel(p2)
            (i,j,z3,phi3) = hf.pixmap.getCoordsForPixel(p3)
            (x1,y1,h1,in1) = cache[p1]
            (x2,y2,h2,in2) = cache[p2]
            (x3,y3,h3,in3) = cache[p3]
            if in1 or in2 or in3:
                havg = (h1+h2+h3)/3.0
                yield (((x1,y1),(x2,y2),(x3,y3)),havg)
