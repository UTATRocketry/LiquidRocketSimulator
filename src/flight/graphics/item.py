import graphics.screen
import graphics.face
import graphics.vertex
import numpy as np

class Item:
    def _update_v_offset(self, n_points=None):
        if self.prev_item==None:
            v_offset = 0
        else:
            v_offset = self.prev_item.next_v_offset
        if n_points==None:
            n_points = len(self.points)
        self.next_v_offset = v_offset + n_points
        return v_offset

    def _writePoints(self, points):
        self.points = []
        for point in points:
            self.points.append(graphics.vertex.Vertex(point))

    def _writeTriangles(self, triangles):
        self.triangles = []
        for triangle in triangles:
            if len(triangle) == 3:
                if self.color != None:
                    triangle.append(self.color)
                else:
                    triangle.append('gray')
                triangle.append(self.border)
            elif len(triangle) == 4:
                triangle.append(self.border)
            self.triangles.append(graphics.face.Face(triangle))

    def __init__(self, name, points=None, triangles=None, prev_item=None, color=None, border='black'):
        self.prev_item = prev_item
        self.color = color
        self.border = border
        if points==None or triangles==None:
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
                        newCoords.append(int(coord))

                    if coords[0]=='w':
                        newCoords.append('white')
                    elif coords[0]=='r':
                        newCoords.append('red')

                    triangles.append(newCoords)
                f.close()

        v_offset = self._update_v_offset(len(points))
        for i in range(len(triangles)):
            for j in range(3):
                triangles[i][j] += v_offset - 1

        self.initial_points = points
        self.initial_triangles = triangles

        self._writePoints(points)
        self._writeTriangles(triangles)

    def rotate(self, axis, angle):
        #rotate model around axis
        if np.isnan(angle):
            angle = 0
        for point in self.points:
            point.rotate(axis, angle)

    def move(self, axis, value):
        for point in self.points:
            point.move(axis, value)

    def move_to(self, value):
        self.move('x',value[0])
        self.move('y',value[1])
        self.move('z',value[2])

    def restore(self):
        self._writePoints(self.initial_points)
        self._writeTriangles(self.initial_triangles)

    def update(self):
        self._update_v_offset()


class LineItem(Item):
    def __init__(self, name, line_points, prev_item=None, color='black'):
        self.prev_item = prev_item
        self.color = color
        self.border = color
        points = []
        points.append(line_points[0])
        for p in line_points[1:]:
            points.append(p)
            points.append(p)
        triangles = []
        indx = 1
        for _ in range(len(line_points)-1):
            newCoords = [indx, indx+1, indx+2]
            triangles.append(newCoords)
            indx += 2

        v_offset = super()._update_v_offset(len(points))
        for i in range(len(triangles)):
            for j in range(3):
                triangles[i][j] += v_offset - 1

        super()._writePoints(points)
        super()._writeTriangles(triangles)

        self.initial_points = self.points
        self.initial_triangles = self.triangles

    def add_point(self, point):
        self.points.append(graphics.vertex.Vertex(point))
        self.points.append(graphics.vertex.Vertex(point))
        last_indx = self.triangles[-1].c
        triangle = [last_indx, last_indx+1, last_indx+2]
        if self.color != None:
            triangle.append(self.color)
        else:
            triangle.append('gray')
        triangle.append(self.border)
        self.triangles.append(graphics.face.Face(triangle))
        super().update()
