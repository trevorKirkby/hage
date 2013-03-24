import world.heightfield
import world.healpix
import world.projection

hf = world.heightfield.Heightfield('world/data/poodle.40.hf',40)
print hf.getHeight(100)
print hf.pixmap.getCoordsForPixel(100)
print hf.pixmap.getCoordsForPixel(4000)
print hf.pixmap.getCoordsForPixel(19000)
hf.pixmap.selfTest()

pm = world.healpix.HEALPixMap(2)
for tri in pm.getMesh():
    print tri

proj = world.projection.Projector(1,0.1)
(dphi,dz) = proj.project(-1.3,0.2)
print (dphi,dz),proj.unproject(dphi,dz)
