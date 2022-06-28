import numpy as np
import matplotlib.pyplot as plt

class Point(): #Point object, with coordinates
    def __init__(self, id = None, x = None, y = None):
        self.id = id                   #ID number of the point
        self.x = x                     #X coordinate of the point
        self.y = y                     #Y coordinate of the point

class DragonCurve(): #Main object
    def __init__(self, i_nr = 0, a = 90, pcolor = (0, 0, 0), ecolor = (0, 0, 0),
                 start = (0.0, 0.0), end = None,
                 e = 400.0, h = 480.0, w = 640.0, r = 0.0):
        self.i_nr = i_nr               #Level of the curve, number of iterations
        self.angle = a                 #Angle of the bend in degrees
        self.edge_length = e           #Length of a unit edge
        
        startp = Point(id = 0, x = start[0], y = start[1])
        self.start = startp            #Point of the starting position
        self.width = w                 #Width of canvas in pixels
        self.height = h                #Height of canvas in pixels
        self.rotate = r                #Angle of rotaion
        
        self.points = []               #Array of ordered points
        self.pcolor = pcolor           #Array of RGB values of the point color
        self.ecolor = ecolor           #Array of RGB values of the edge color
        self.highlights = None         #Array of highligted points
        self.hcolor = None             #Array of arrays of RGB values of the highlighted points color
        
        self.points.append(startp)
        
        if end == None:
            endp = Point(id = startp.id + 1, x = startp.x, y = startp.y + self.edge_length)
        else:
            endp = end
        
        self.points.append(endp)
        
        for i in range(i_nr):
            self.iterate()
    
    def iterate(self):
        newpoints = []
        newpoints.append(self.points[0])
        
        #Special case, angle is 90 degrees
        if self.angle == 90.0:
            sign = -1
            
            for i in range(len(self.points) - 1):
                p1 = self.points[i]
                p2 = self.points[i + 1]
                midp = [(p1.x + p2.x) / 2.0, (p1.y + p2.y) / 2.0]

                #Half of the distance between the 2 original points
                distance = (((p2.x - p1.x)**2.0 + (p2.y - p1.y)**2.0)**0.5) / 2.0
                
                #Angle of the line relative to the screen
                #http://jsfiddle.net/92jWG/5/
                #https://stackoverflow.com/questions/17989148/javascript-find-point-on-perpendicular-line-always-the-same-distance-away
                angle = np.arctan2(p2.y - p1.y, p2.x - p1.x)

                #Points between p1 and p2, the original is p12 and the mirror is p21
                #Choose based on the sign
                if sign == 1:
                    p12 = Point(id = newpoints[-1].id + 1, 
                                x = np.around(np.sin(angle) * distance + midp[0], decimals = 14),
                                y = np.around(- np.cos(angle) * distance + midp[1], decimals = 14))
                    newpoints.append(p12)
                else:
                    p21 = Point(id = newpoints[-1].id + 1, 
                                x = np.around(- np.sin(angle) * distance + midp[0], decimals = 14),
                                y = np.around(np.cos(angle) * distance + midp[1], decimals = 14))
                    newpoints.append(p21)
                
                sign *= -1

                p2 = Point(id = newpoints[-1].id + 2, x = p2.x, y = p2.y)
                newpoints.append(p2)

        self.points = newpoints

fig = plt.figure()
ax = fig.add_subplot(111)
        

TestCurve = DragonCurve(i_nr = 10)

X, Y = [], []

for p in TestCurve.points:
    X.append(p.x)
    Y.append(p.y)

plt.plot(X, Y, c='k', lw=2)#, marker='o')

for i in range(TestCurve.i_nr):
    o = TestCurve.points[2**(i+1)]
    Xo = [o.x]
    Yo = [o.y]
    plt.plot(Xo, Yo, c='b', marker='o')

plt.axes().set_aspect('equal', 'datalim')
plt.show()
