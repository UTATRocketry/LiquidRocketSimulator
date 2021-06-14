import graphics.screen
import graphics.face
import graphics.vertex

class Item:
    def writePoints(self, points):
        self.points = []
        for point in points:
            self.points.append(graphics.vertex.Vertex(point))

    def writeTriangles(self, triangles):
        self.triangles = []
        for triangle in triangles:
            if len(triangle) != 4:
                triangle.append('gray')
            self.triangles.append(graphics.face.Face(triangle))

    def __init__(self, name, v_offset=0):
        points = []
        triangles = []
        with open('graphics/'+name+'V.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                coords = line[:-2].split(' ')
                points.append([-1*float(coords[0]), -1*float(coords[1]), -1*float(coords[2])])
            f.close()

        with open('graphics/'+name+'T.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                coords = line[:-2].split(' ')
                newCoords = []
                for coord in coords[1:4]:
                    newCoords.append(int(coord) - 1 + v_offset)
                triangles.append(newCoords)
            f.close()

        self.writePoints(points)
        self.writeTriangles(triangles)

        self.initial_points = self.points
        self.initial_triangles = self.triangles

    def rotate(self, axis, angle):
        #rotate model around axis
        for point in self.points:
            point.rotate(axis, angle)

    def move(self, axis, value):
        for point in self.points:
            point.move(axis, value)