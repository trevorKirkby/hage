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
        print (dx,dy,dz)
        return (math.atan2(dy,dx),dz)
    """
    Performs the inverse projection where dphi is in radians and returns the
    absolute phi in the range (-pi,2pi) and z in the range (-1,+1)
    """
    def unproject(self,dphi,dz):
        st = math.sqrt(1-dz*dz)
        cp = math.cos(dphi)
        sp = math.sin(dphi)
        x = self.cp0ct0*cp*st - self.sp0*sp*st - self.cp0z0*dz
        y = self.cp0*sp*st + self.sp0ct0*cp*st - self.sp0z0*dz
        z = self.ct0*dz + self.z0*cp*st
        return (math.atan2(y,x),z)
