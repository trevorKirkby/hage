import world.heightfield
import world.projection

hf = world.heightfield.Heightfield('world/data/poodle.20.hf',20)
map = world.projection.ProjectedMap(0,0,800,400)
map.setAbsoluteCenter(0,0)
map.setAbsoluteScale(10)

for points in map.render(hf):
    print points
