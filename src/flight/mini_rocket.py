'''
The Python 3D rendering engine is adapted from
https://github.com/hnhaefliger/pyEngine3D
'''
import graphics.engine

points = []
triangles = []

with open('graphics/RocketV.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        coords = line[:-2].split(' ')
        points.append([float(coords[0]), float(coords[1]), float(coords[2])])
    f.close()

with open('graphics/RocketT.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        coords = line[:-2].split(' ')
        newCoords = []
        for coord in coords[1:4]:
            newCoords.append(int(coord)-1)
        triangles.append(newCoords)
    f.close()

test = graphics.engine.Engine3D(points, triangles, title='Rocket', background='cyan')
test.render()
test.screen.window.mainloop()