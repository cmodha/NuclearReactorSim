#A simple calculation of critical mass(radius)

import random as rand
import matplotlib.pyplot as plt
import math
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
PI = 3.1415926535
e = 2.7182818284590452353602874713527

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

def randWalk(x,y,z,R):#Runs a random walk for one starting position
    (lat, long) = randVect()#Gives a random starting direction
    Absorbed = False
    Exceeded = False
    Fissioned = False
    #-------Values----------------------------------
    l = 2.78  #Cm
    sigA = 0.095#Barns
    sigS = 4.409+1.917#Barns 
    step = 0.01
    sigF = 1.219#Barns
    sigT = sigA+sigS+sigF#Barns
    #--------------------------------------------------
    probA = sigA/sigT
    probF = sigF/sigT
    R2 = R*R
    while (not Absorbed) and (not Exceeded) and (not Fissioned):
        #We take a step of l/4 and randomly decide if the neutron has interacted with an atom or not
        if rand.random()>np.power(e, -step):#If the neutron has interacted with an atom
             
            if rand.random()<probF:#If particle Fissioned
                Fissioned = True
                
            else:
                if rand.random()<probA:#If particle absorbed
                    Absorbed = True
                    
                else:
                    (lat, long) = randVect()#Particle has been scattered
                    
        x = x+step*l*math.sin(lat)*math.cos(long)
        y =y+step*l*math.sin(lat)*math.sin(long)
        z =z+step*l*math.cos(lat)
        if (x*x+y*y+z*z)>R2:
            Exceeded = True
    
    return Fissioned, Absorbed

Rs = []
ks = []
for R in np.linspace(5, 10, 20):  
    numberFissioned = 0
    numberAbsorbed = 0
    n = 10000
    for i in range(n):#Run lots of neutrons for one radius
        (x,y,z) = randUnitPoint()
        Fissioned, Absorbed = randWalk(x,y,z,R)
        if Fissioned:
            numberFissioned +=1
        if Absorbed:
            numberAbsorbed +=1
        k = 2.53*numberFissioned/n
    print(numberFissioned/n, numberAbsorbed/n, 1-(numberFissioned+numberAbsorbed)/n)
        
    ks.append(k)
    Rs.append(R)


fig = plt.figure()
ax = fig.add_subplot(111)
#fig1 = plt.figure()
#ax1 = fig1.add_subplot(111, projection='3d')
#for path in paths:
   # ax1.plot(path[0],path[1],path[2])
ax.scatter(Rs,ks)
print("Rawr XD!")