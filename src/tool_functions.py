import numpy, math
POINTS=None
COLORS=None
cube_length = None

class Tool(object):
    def __init__(self):
        pass
        
    def onMousePress(self, button, state, x, y):
        pass
        
class CubeTool(Tool):
    def __init__(self, r):
        super(CubeTool, self).__init__()
        self.radius = r
        
    def onMousePress(self, x,y,z):
        radius = self.radius
        print "Sphere.onMousePress " + str(x) + " " + str(y) + " " + str(z)
        for i in range(x-radius, x+radius):
            for j in range(y-radius, y+radius):
                for k in range(z-radius, z+radius):
                    if i>=0 and j>=0 and k>=0 and i <cube_length and j <cube_length and k < cube_length:
                        COLORS[i*cube_length**2+j*cube_length+k] = [0,0,0]
        
class PlaneTool(Tool):
    def __init__(self, halfLength):
        super(PlaneTool, self).__init__()
        self.halfLength = halfLength
        
    def onMousePress(self, x,y,z):
        tempx = math.fabs(x-self.halfLength)
        tempy = math.fabs(y-self.halfLength)
        tempz = math.fabs(z-self.halfLength)
        if tempx > tempy and tempx > tempz:
            if x > self.halfLength:
                for i in range(x,cube_length):
                    for j in range(cube_length):
                        for k in range(cube_length):
                            COLORS[i*cube_length**2+j*cube_length+k] = [0,0,0]
            else:
                for i in range(0,x):
                    for j in range(cube_length):
                        for k in range(cube_length):
                            COLORS[i*cube_length**2+j*cube_length+k] = [0,0,0]
        elif tempy > tempz:
            if y > self.halfLength:
                for j in range(y,cube_length):
                    for k in range(cube_length):
                        for i in range(cube_length):
                            COLORS[i*cube_length**2+j*cube_length+k] = [0,0,0]
            else:
                for j in range(0,y):
                    for k in range(cube_length):
                        for i in range(cube_length):
                            COLORS[i*cube_length**2+j*cube_length+k] = [0,0,0]
        else:
            if z > self.halfLength:
                for k in range(z,cube_length):
                    for i in range(cube_length):
                        for j in range(cube_length):
                            COLORS[i*cube_length**2+j*cube_length+k] = [0,0,0]
            else:
                for k in range(0,z):
                    for i in range(cube_length):
                        for j in range(cube_length):
                            COLORS[i*cube_length**2+j*cube_length+k] = [0,0,0]
        