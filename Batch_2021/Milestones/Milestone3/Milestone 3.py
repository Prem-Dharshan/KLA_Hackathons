#Milestone 3

import math
import numpy as np

f=open('Input/Testcase1.txt', 'r')
inp={}
for l in f.readlines():
    l=l.strip().split(':')
    inp[l[0]]=l[1]
print(inp)

class Wafer:
    def __init__(self, diameter):
        self.diameter=int(diameter)
    def setDiameter(self, dia):
        self.diameter=dia
    def getDiameter(self):
        return self.diameter

class Reticle:
    def __init__(self, diesize, diestreet, reticlestreet, dieno, shift):
        self.dieno=[int(i) for i in dieno.split('x')]
        self.dsWidth=int(diestreet.split(',')[0][1:])
        self.dsHeight=int(diestreet.split(',')[1][:-1])
        self.rWidth=int(reticlestreet.split(',')[0][1:])
        self.rHeight=int(reticlestreet.split(',')[1][:-1])
        self.dwidth=int(diesize.split('x')[0])
        self.dheight=int(diesize.split('x')[1])
        self.height=self.dieno[0]*self.dheight+self.dieno[0]*self.dsHeight+self.rHeight
        self.width=self.dieno[1]*self.dwidth+self.dieno[1]*self.dsWidth+self.rWidth
        self.shiftx=int(shift.split(',')[0][1:])
        self.shifty=int(shift.split(',')[1][:-1])
    def __str__(self):
        return("Width: "+str(self.width)+" Height: "+str(self.height))

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

r1=Reticle(inp['DieSize'], inp['DieStreetWidthAndHeight'], inp['RecticleStreetWidthAndHeight'], inp['DiesPerReticle'], inp['DieShiftVector'])
print(r1)


ilim=referDie.getLLC()[0]
ic=0

while(ilim+Die.width>-wafer1.diameter/2):
    if ilim-r1.shiftx%r1.width==0:
        print(ilim)
        ilim-=r1.dwidth-r1.dsWidth-r1.rWidth
        ic+=1
    else:
        print(ilim)
        ilim-=r1.dwidth-r1.dsWidth
        ic+=1

jc=0
jlim=referDie.getLLC()[1]
while(jlim+Die.height>-wafer1.diameter/2):
    if jlim-r1.shifty%r1.height==0:
        print(jlim)
        jlim-=r1.dheight-r1.dsHeight-r1.rHeight
        jc+=1
    else:
        print(jlim)
        jlim-=r1.dheight-r1.dsHeight
        jc+=1

print(ilim, jlim)
Dies=[]
i=ilim

#ic-=1
#jc-=1

while i<(wafer1.diameter/2):
    row=[]
    j=jlim
    while j<(wafer1.diameter/2):
        print(i, j)
        llc=Point((int(i), int(j)))
        ind=Point(referDie.calculateIndex(llc))
        print(ind)
        row.append(Die(ind, llc))
        if j+r1.shifty%80==0:
            j+=r1.dheight+r1.dsHeight+r1.rHeight
            jc-=1
        else:
            j+=Die.height+r1.dsHeight
            jc-=1
    Dies.append(row)
    if (i+r1.shiftx%r1.height==0):
        i+=r1.dwidth+r1.dsWidth+r1.rWidth
        ic-=1
    else:
        i+=Die.width+r1.dsWidth
        ic-=1


print(Point((125, 108)).inCircle(150))
writeFile=open('Testcase1_output.txt', 'w')
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
writeFile.write(str(referDie))
writeFile.close()
