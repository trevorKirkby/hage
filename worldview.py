import world.heightfield, world.projection

hf = world.heightfield.Heightfield('world/data/poodle.20.hf',20)
mp = world.projection.ProjectedMap(0,0,800,400)
mp.setAbsoluteCenter(0,0)
mp.setAbsoluteScale(10)

for points in mp.render(hf):
    print points
