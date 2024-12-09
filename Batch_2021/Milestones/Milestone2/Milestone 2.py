#Milestone 2

import math
import numpy as np

f=open('Input/Testcase3.txt', 'r')
inp={}
for l in f.readlines():
    l=l.strip().split(':')
    inp[l[0]]=l[1]

class Wafer:
    def __init__(self, diameter):
        self.diameter=int(diameter)
    def setDiameter(self, dia):
        self.diameter=dia
    def getDiameter(self):
        return self.diameter

class Point:
    def __init__(self, point):
        if isinstance(point, str):
            self.x=int(point.split(',')[0][1:])
            self.y=int(point.split(',')[1][:-1])
        elif isinstance(point, tuple):
            self.x=point[0]
            self.y=point[1]
    def __str__(self):
        return ("("+str(self.x)+","+str(self.y)+")")
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
    
    def getDistance(self):
        return math.sqrt(self.x**2+self.y**2)
    
    def inCircle(self, r):
        if self.getDistance()>=r:
            return False
        else:
            return True

class Die:
    width=int(inp['DieSize'].split('x')[0])
    height=int(inp['DieSize'].split('x')[1])
    shift=Point(inp['DieShiftVector'])
    def __init__(self, index, llc):
        self.index=index
        self.llc=Point((llc.getX(), llc.getY()))

    def __str__(self):
        return (str(self.index)+":"+str(self.llc))

    def getSize(self):
        return (self.height, self.width)
    
    def getHeight(self):
        return(self.height)
    
    def getWidth(self):
        return(self.width)
    
    def getShift(self):
        return(self.shift)
    
    def getIndex(self):
        return(self.index.getPoint())
    
    def getLLC(self):
        return(self.llc.getPoint())

    def calculateIndex(self, llc1):
        indx=int((llc1.getX()-self.llc.getX())/Die.width)
        indy=int((llc1.getY()-self.llc.getY())/Die.height)
        return (indx, indy)

wafer1=Wafer(inp['WaferDiameter'])
refllc=Point(inp['ReferenceDie'])
refllc.setX(int(refllc.getX()-Die.width/2))
refllc.setY(int(refllc.getY()-Die.height/2))
print(refllc)
referDie=Die(Point((0, 0)), refllc)
print(referDie)


ilim=referDie.getLLC()[0]
while(ilim+Die.width>-wafer1.diameter/2):
    print(ilim)
    ilim-=Die.width

jlim=referDie.getLLC()[1]
while(jlim+Die.height>-wafer1.diameter/2):
    print(jlim)
    jlim-=Die.height

print(ilim, jlim)
Dies=[]
i=ilim
while i<(wafer1.diameter/2):
    row=[]
    j=jlim
    while j<(wafer1.diameter/2):
        print(i, j)
        llc=Point((int(i), int(j)))
        ind=Point(referDie.calculateIndex(llc))
        print(ind)
        row.append(Die(ind, llc))
        j+=Die.height
    Dies.append(row)
    i+=Die.width


print(Point((125, 108)).inCircle(150))
writeFile=open('Testcase3_output.txt', 'w')
r=wafer1.diameter/2
for row in Dies:
    #print('[', end="")
    for column in row:
        print(str(column), end="")
        llc=Point(column.getLLC())
        lrc=Point((llc.x, llc.y+Die.height))
        ulc=Point((llc.x+Die.width, llc.y))
        urc=Point((llc.x+Die.width, llc.y+Die.height))
        if(urc.inCircle(r) or ulc.inCircle(r) or llc.inCircle(r) or lrc.inCircle(r)):
            print("in")
            writeFile.write(str(column)+'\n')
        else:
            print(urc.getDistance(), ulc.getDistance(), llc.getDistance(), lrc.getDistance())

writeFile.close()