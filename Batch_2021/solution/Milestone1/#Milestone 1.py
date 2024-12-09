#Milestone 1
import json
import math
import numpy as np

for fileNo in range(4):

    f=open("Input/Testcase"+str(fileNo+1)+".txt")
    inp={}

    class Wafer:
        def __init__(self, diameter=0):
            self.diameter=diameter
        def setDiameter(self, dia):
            self.diameter=dia
        def getDiameter(self):
            return self.diameter

    class Point:
        def __init__(self, x=0, y=0):
            self.x=x
            self.y=y
        def __str__(self):
            return ("X: "+str(self.x)+" Y: "+str(self.y))
        def getPoint(self):
            return (self.x, self.y)
        def getX(self):
            return self.x
        def getY(self):
            return self.y
        def setX(self, x):
            self.x=x
        def setY(self, y):
            self.y=y
        def computePoint(self, r, t, p1):
            self.x=r*math.cos(t*(math.pi/180))+p1.getX()
            self.y=r*math.sin(t*(math.pi/180))+p1.getY()

    wafer1=Wafer()

    for l in f.readlines():
        l=l.split(':')
        if l[0]=='WaferDiameter':
            wafer1.setDiameter(float(l[1].strip()))
        inp[l[0]]=float(l[1].strip())

    #x = r * cos(A) + x0; y = r * sin(A) + y0;

    p1=Point(0, 0)
    #First Corner Point

    corner1=Point()
    corner1.computePoint(wafer1.diameter/2, inp['Angle'], p1)
    corner2=Point(-corner1.getX(), -corner1.getY())

    points=(np.linspace(corner1.getPoint(), corner2.getPoint(), int(inp['NumberOfPoints'])))
    #print(points)
    ind = np.lexsort((points[:,1],points[:,0]))    
    points=points[ind]

    writeFile=open('TestCase'+str(fileNo+1)+'_output.txt', 'w')
    for point in points:
        writeFile.write('('+str(point[0].round(4))+','+str(point[1].round(4))+')\n')

    writeFile.close()

