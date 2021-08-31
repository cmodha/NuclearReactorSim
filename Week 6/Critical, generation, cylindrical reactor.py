
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
generations = 30#Value
#--------------------------------------------------
probA = sigA/sigT
probF = sigF/sigT



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

def exceeded(x,y,z,R2,L):#This defines the geometry of the uranium
    Exceeded = False
    if (x*x+y*y)> R2:
        Exceeded = True
    if abs(z)>L/2:
        Exceeded = True
    return Exceeded

def samplePoints(points,N):#Takes a smaple of N neutrons produced by fissions in a generation.
    
    length = len(points)#Number of fissioned neutrons in previous generation
    
    if length>=N:#If >100 neutrons to sample from: choose randomly
        #print('length>')
        newPoints = []#Will store the smapled points from the previous generation
        for i in range(0,N):
            
            randIndex = rand.randint(0,length-1)
            newPoints.append(points[randIndex])
            points.pop(randIndex)
            length-=1
    else:#If <100 neutrons to sample from: Double sample some points untill length= N
        newPoints = points
        #print('length<')
        for i in range(0, N-length):
            randIndex = rand.randint(0,length-1)
            #print(rand.randint(0,3))
            newPoints.append(points[randIndex])
            #print(len(newPoints))
    #print('length of sample: ',len(newPoints))
    return newPoints

def randWalk(point,R2,L):#Runs a random walk for one starting position
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
        Exceeded = exceeded(x,y,z,R2,L)
        
    
    point = [x,y,z,lat,long]
    return point, Fissioned, Absorbed, Exceeded#Return the position and direction of the neutron when it is absorbed


#We run this program over different R and L values and plot <k> against them

def runGenerations(R, L):
    R2 = R*R
    newPoints = seedStart(N)
    ks = []
    for i in range(generations):
        points = samplePoints(newPoints, N)
        newPoints = []
        numberFissioned = 0
        
        for i in range(0,1000):#Run through every point
            
            newPoint, Fissioned, Absorbed, Exceeded = randWalk(points[i],R2,L)
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
        avK =0
        ks.append(k)
    for i in range(10, len(ks)):
        avK += ks[i]/(generations-10)

    print('avK: ',avK)
    return avK

#Run our code through several values of R and L and record av of k
avKs = []
Rs = []
Ls = []
fig1 = plt.figure()
ax1 = fig1.add_subplot(111, projection='3d')
for R in np.linspace(5, 10, 5):
    for L in np.linspace(12, 17, 5):
        print('Start:')
        print('R: ', R, ', L: ',L)
        avK = runGenerations(R, L)
        avKs.append(avK)
        Rs.append(R)
        Ls.append(L)
        print('End\n')
ax1.scatter(Rs,Ls,avKs)
print("Rawr XD!")
plt.show()
