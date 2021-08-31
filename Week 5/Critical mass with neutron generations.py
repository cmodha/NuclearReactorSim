
#A program to calculate the distribution function n(r) of neutrons inside a sphere of uranium 235

import random as rand
import matplotlib.pyplot as plt
import math
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
PI = 3.1415926535
e = 2.7182818284590452353602874713527
N = 1000#Number of neutrons per generation

def randVect():#Generates a random direction on the unit sphere, definted by x,y,z.
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
        lat, long = randVect()
        points.append([x,y,z,lat,long])
    return points


def samplePoints(points,N):#Takes a smaple of 100 neutrons produced by fissions in a generation.
    oldPoints = points
    
    length = len(oldPoints)#Number of fissioned neutrons in previous generation
    
    newPoints= []#Will store the smapled points from the previous generation
    if length>=N:#If >100 neutrons to sample from: choose randomly
        for i in range(0,N):
            
            randIndex = rand.randint(0,length-1)

            newPoints.append(oldPoints[randIndex])
            oldPoints.pop(randIndex)
            
            length-=1
    else:#If <100 neutrons to sample from: Use all available and fill make length up to 100 with zeros
        newPoints = oldPoints
        for i in range(0, N-length):
            newPoints.append([0,0,0,0,0])
    return newPoints







def randWalk(point, R):#Runs a random walk for one starting position
    
    Absorbed = False
    Exceeded = False
    Fissioned = False
    #-------Values----------------------------------
    l = 2.73 #Cm
    sigA = 0.095#Barns
    sigS = 4.409+1.917#Barns 
    step = 0.1
    sigF = 1.219#Barns
    sigT = sigA+sigS+sigF#Barns
    #--------------------------------------------------
    probA = sigA/sigT
    probF = sigF/sigT
    R2 = R*R
    x = point[0]
    y = point[1]
    z = point[2]
    lat = point[3]
    long = point[4]
    #------------------------------------------
    if point != [0,0,0,0,0]:#Only ru
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
    return point, Fissioned, Absorbed#Return the position and direction of the neutron when it is absorbed

Rs = []
ks = []
fissionPoints = []
R = 30#value
fissionPoints = seedStart(N)

for i in range(10):
    points = samplePoints(fissionPoints, N)
    fissionPoints.clear()
    for point in points:#Run through every point 
        point, Fissioned, Absorbed = randWalk(point,R)
        x = point[0]
        y = point[1]
        z = point[2]
        if Fissioned:
            #numberFissioned +=1
            if rand.random()<=0.5:#Half the time we produce 2 new neutrons with random velocities
                (lat,long) = randVect()
                fissionPoints.append([x,y,z,lat,long])
                (lat,long) = randVect()
                fissionPoints.append([x,y,z,lat,long])
            else:#Half the time we produce 3 new neutrons with random velocities
                (lat,long) = randVect()
                fissionPoints.append([x,y,z,lat,long])
                (lat,long) = randVect()
                fissionPoints.append([x,y,z,lat,long])
                (lat,long) = randVect()
                fissionPoints.append([x,y,z,lat,long])
        


fig = plt.figure()
ax = fig.add_subplot(111)
fig1 = plt.figure()
ax1 = fig1.add_subplot(111, projection='3d')
rs = []
for point in fissionPoints:
    x = point[0]
    y = point[1]
    z = point[2]
    r = np.sqrt(x*x+y*y+z*z)
    rs.append(r)
ax.hist(rs, bins = 50)

for point in fissionPoints:#Plot the location of the points where neutrons were produced(fission points)
    ax1.scatter(point[0],point[1],point[2])

print("Rawr XD!")