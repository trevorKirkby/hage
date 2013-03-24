import world.heightfield

hf = world.heightfield.Heightfield('world/data/poodle.40.hf',40)
print hf.getHeight(100)
print hf.pixmap.getPixel(100)
print hf.pixmap.getPixel(4000)
print hf.pixmap.getPixel(19000)