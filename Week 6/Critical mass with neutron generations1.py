
#A program to calculate the distribution function n(r) of neutrons inside a sphere of uranium 235

import random as rand
import matplotlib.pyplot as plt
import math
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
PI = 3.1415926535
e = 2.7182818284590452353602874713527
N = 1000#Number of neutrons per generation
 #-------Values----------------------------------
l = 2.73 #Cm
sigA = 0.095#Barns
sigS = 4.409+1.917#Barns 
step = 0.1
sigF = 1.219#Barns
sigT = sigA+sigS+sigF#Barns
R = 8.55#value
generations = 100#Value
#--------------------------------------------------
probA = sigA/sigT
probF = sigF/sigT
R2 = R*R


def randVect():#Generates a random direction on the unit sphere, defined by x,y,z.
    longitude = rand.random()*2*PI
    latitude  = math.acos(1-2*rand.random())

    return latitude, longitude

def randUnitPoint():#Generates a random point within the unit sphere
    discarded = True
    while discarded:
        x = 1-2*rand.random()
        y = 1-2*rand.random()
        z = 1-2*rand.random()
        if (x*x+y*y+z*z)<1:#Only return point if r<1
                 discarded = False
                 
    return (x,y,z)




def seedStart(N):#Seeds the starting positions of neutrons for the first generation
    points = []
    for i in range(N):
        (x,y,z) = randUnitPoint()
        x=R*x
        y=R*y
        z=R*z
        lat, long = randVect()
        points.append([x,y,z,lat,long])
    return points



def samplePoints(points,N):#Takes a smaple of N neutrons produced by fissions in a generation.
    
    length = len(points)#Number of fissioned neutrons in previous generation
    
    if length>=N:#If >100 neutrons to sample from: choose randomly
        print('length>')
        newPoints = []#Will store the smapled points from the previous generation
        for i in range(0,N):
            
            randIndex = rand.randint(0,length-1)
            newPoints.append(points[randIndex])
            points.pop(randIndex)
            length-=1
    else:#If <100 neutrons to sample from: Double sample some points untill length= N
        newPoints = points
        print('length<')
        for i in range(0, N-length):
            randIndex = rand.randint(0,length-1)
            #print(rand.randint(0,3))
            newPoints.append(points[randIndex])
            #print(len(newPoints))
    print('length of sample: ',len(newPoints))
    print(newPoints[999])
    return newPoints







def randWalk(point):#Runs a random walk for one starting position
    Absorbed = False
    Exceeded = False
    Fissioned = False
    x = point[0]
    y = point[1]
    z = point[2]
    lat = point[3]
    long = point[4]
    #------------------------------------------
    
    while (not Absorbed) and (not Exceeded) and (not Fissioned):
        #We take a step of l/4 and randomly decide if the neutron has interacted with an atom or not
        if rand.random()>np.power(e, -step):#If the neutron has interacted with an atom
             
            if rand.random()<probF:
                Fissioned = True
                
            else:
                if rand.random()<probA:
                    Absorbed = True
                    
                else:
                    (lat, long) = randVect()#Particle has been scattered
                    
        x = x+step*l*math.sin(lat)*math.cos(long)
        y =y+step*l*math.sin(lat)*math.sin(long)
        z =z+step*l*math.cos(lat)
        if (x*x+y*y+z*z)>R2:
            Exceeded = True
        
    
    point = [x,y,z,lat,long]
    return point, Fissioned, Absorbed, Exceeded#Return the position and direction of the neutron when it is absorbed

Rs = []
ks = []
fissionPoints = []

newPoints = seedStart(N)

for i in range(generations):
    print('start:')
    print(len(newPoints))
    points = samplePoints(newPoints, N)
    print(points[0])
    newPoints = []
    numberFissioned = 0
    
    for i in range(0,1000):#Run through every point
        
        newPoint, Fissioned, Absorbed, Exceeded = randWalk(points[i])
        x = newPoint[0]
        y = newPoint[1]
        z = newPoint[2]
        latitude = newPoint[3]
        longitude = newPoint[4]
        if Fissioned:
            numberFissioned +=1
            if rand.random()<=0.5:#Half the time we produce 2 new neutrons with random velocities
                for i in range(0,2):
                    (lat,long) = randVect()
                    newPoints.append([x,y,z,lat,long])
            else:#Half the time we produce 3 new neutrons with random velocities
                for i in range(0,3):
                    (lat,long) = randVect()
                    newPoints.append([x,y,z,lat,long])
        if (not Absorbed) and (not Exceeded):
            newPoints.append([x,y,z,latitude,longitude])
    k = 2.5*numberFissioned/N
    ks.append(k)
    print('k: ', k)
    print(len(newPoints))
    print('end: \n\n')
fig = plt.figure()
ax = fig.add_subplot(111)
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
rs = []
for point in newPoints:
    x = point[0]
    y = point[1]
    z = point[2]
    r = np.sqrt(x*x+y*y+z*z)
    rs.append(r)
ax.hist(rs, bins = 50)

ax1.scatter(range(generations),ks)
avK =0
for i in range(10, len(ks)):
    avK += ks[i]/(generations-10)

print('Averatge k: ', avK)
print("Rawr XD!")
plt.show()
