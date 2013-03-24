import world.heightfield

hf = world.heightfield.Heightfield('world/data/poodle.40.hf',40)
print hf.getHeight(100)
print hf.pixmap.getCoordsForPixel(100)
print hf.pixmap.getCoordsForPixel(4000)
print hf.pixmap.getCoordsForPixel(19000)
hf.pixmap.selfTest()
