import world.heightfield
import world.healpix

hf = world.heightfield.Heightfield('world/data/poodle.40.hf',40)
print hf.getHeight(100)
print hf.pixmap.getCoordsForPixel(100)
print hf.pixmap.getCoordsForPixel(4000)
print hf.pixmap.getCoordsForPixel(19000)
hf.pixmap.selfTest()

pm = world.healpix.HEALPixMap(2)
mesh = pm.getMesh()
for tri in mesh:
    print tri
print 'mesh size =',len(mesh)
