import numpy
POINTS=None
COLORS=None
cube_length = None

class Tool(object):
    def __init__(self):
        pass
        
    def onMousePress(self, button, state, x, y):
        pass
        
class CubeTool(Tool):
    def __init__(self):
        super(CubeTool, self).__init__()
        self.radius = 3
        
    def onMousePress(self, x,y,z):
        radius = self.radius
        print "Sphere.onMousePress " + str(x) + " " + str(y) + " " + str(z)
        for i in range(x-radius, x+radius):
            for j in range(y-radius, y+radius):
                for k in range(z-radius, z+radius):
                    if i>=0 and j>=0 and k>=0 and i <cube_length and j <cube_length and k < cube_length:
                        COLORS[i*cube_length**2+j*cube_length+k] = [0,0,0]
        
        