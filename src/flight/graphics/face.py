class Face:
    def __init__(self, vertices):
        #store point indexes
        (a, b, c, color, border) = vertices
        self.a = a
        self.b = b
        self.c = c
        self.color = color
        self.border = border
