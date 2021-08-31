#This program simulates neutrons inside a reactor.  We run through a neutron from life to death
#We record the distance travelled by several neutrons

import random as rand
import matplotlib.pyplot as plt
import math
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
PI = 3.1415926535
e = 2.7182818284590452353602874713527

def randPoint():
    #Generates a random direction on the unit sphere, definted by x,y,z.
    longitude = rand.random()*2*PI
    latitude  = math.acos(1-2*rand.random())

    return latitude, longitude

def randomWalk(x,y,z):
    (lat, long) = randPoint()#Gives a random starting direction
    absorbed = False
    #-------Values----------------------------------
    l = 45 
    sigA = 1.314
    sigT = 7.64
    step = 1
    #--------------------------------------------------
   
    while not absorbed:
        #We take a step of l/4 and randomly decide if the neutron has interacted with an atom or not
        if rand.random()<1-np.power(e, -step):#If the neutron has interacted with an atom
            if rand.random()<(sigA/sigT):
                absorbed = True        
            else:
                (lat, long) = randPoint()
        x = x+step*l*math.sin(lat)*math.cos(long)
        y =y+step*l*math.sin(lat)*math.sin(long)
        z =z+step*l*math.cos(lat)
        
        
    r = np.sqrt(x*x+y*y+z*z)
    return float(r)
    
rs = []#This will store the final distance from the origin of our nutrons
for i in range(100000):
    r = randomWalk(0,0,0)
    rs.append(r)
    
fig = plt.figure()
ax = fig.add_subplot(111)

ax.hist(rs, bins=300)
