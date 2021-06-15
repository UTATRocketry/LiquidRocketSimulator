import graphics.screen
import graphics.face
import graphics.vertex
import numpy as np

class Engine3D:
    def __zero_camera(self, event):
        self.distance = 100
        self.scale = 100
        self.screen.zeros[0] = 500
        self.screen.zeros[1] = 350
        self.camera = np.identity(3)

    def __resetDrag(self, event):
        self.__prev_drag = []
        self.__prev_pan = []

    def __drag(self, event):
        if self.__prev_drag:
            dx = (event.x - self.__prev_drag[0]) / 70
            dy = (event.y - self.__prev_drag[1]) / 70
            self.camera = np.array([[np.cos(-dx),0,np.sin(-dx)],[0,1,0],[-1*np.sin(-dx),0,np.cos(-dx)]]) @ self.camera
            self.camera = np.array([[1,0,0],[0,np.cos(dy),-1*np.sin(dy)],[0,np.sin(dy),np.cos(dy)]]) @ self.camera
            self.clear()
            self.render()
        self.__prev_drag = [event.x, event.y]

    def __pan(self, event):
        if self.__prev_pan:
            self.screen.zeros[0] += event.x - self.__prev_pan[0]
            self.screen.zeros[1] += event.y - self.__prev_pan[1]
            self.clear()
            self.render()
        self.__prev_pan = [event.x, event.y]

    def __zoom(self, event):
        self.distance *= (1 - (event.delta/120)*0.025)
        self.scale *= (1 + (event.delta/120)*0.025)
        self.clear()
        self.render()

    def __rotate(self, axis, angle):
        #rotate model around axis
        # for item in self.items:
        #     item.rotate(axis, angle)
        pass

    def __init__(self, items, width=1000, height=700, distance=100, scale=100, title='3D', background='white'):
        #object parameters
        self.items = items
        self.distance = distance
        self.scale = scale
        self.camera = np.identity(3)

        #initialize display
        self.screen = graphics.screen.Screen(width, height, title, background)
        self.screen.window.bind('<B2-Motion>', self.__drag)
        self.__prev_drag = []
        self.screen.window.bind('<Control-B2-Motion>', self.__pan)
        self.__prev_pan = []
        self.screen.window.bind('<ButtonRelease-2>', self.__resetDrag)
        self.screen.window.bind('<MouseWheel>', self.__zoom)
        self.screen.window.bind('<space>', self.__zero_camera)

    def clear(self):
        #clear display
        self.screen.clear()

    def render(self):
        points = []
        triangles = []
        for item in self.items:
            points += item.points
            triangles += item.triangles

        # rotate points by rotation matrix
        new_points = []
        for point in points:
            new_pt = self.camera @ np.array([point.x,point.y,point.z])
            new_pt = new_pt.tolist()
            new_points.append(graphics.vertex.Vertex(new_pt))

        #calculate flattened coordinates (x, y)
        flattened = []
        for point in new_points:
            flattened.append(point.flatten(self.scale, self.distance))

        #get coordinates to draw triangles
        new_triangles = []
        for triangle in triangles:
            avgZ = -(new_points[triangle.a].z + new_points[triangle.b].z + new_points[triangle.c].z) / 3
            new_triangles.append((flattened[triangle.a], flattened[triangle.b], flattened[triangle.c], triangle.color, triangle.border, avgZ))

        #sort triangles from furthest back to closest
        new_triangles = sorted(new_triangles,key=lambda x: x[5])

        #draw triangles
        for triangle in new_triangles:
            self.screen.createTriangle(triangle[0:3], triangle[3], triangle[4])
