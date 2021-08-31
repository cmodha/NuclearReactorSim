#A program to simulate neutrons in a moderator
#It will record the distance neutrons travel after 6 inelastic scatterings

import random as rand
import matplotlib.pyplot as plt
import math
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
PI = 3.1415926535
e = 2.7182818284590452353602874713527

#-------Values----------------------------------
sigE = 2.37#Elastic Scattering cross section[Barns]
sigIE = 0.012#Inelastic Scattering cross section[Barns]
sigA = 0.00000152#Absorbtion cross seciton [Barns]
step = 0.01#Accuracy variable
sigT = sigE + sigIE + sigA#Barns
   
n = 2.266*6.022*np.power(10,23)/12#Number density [cm^-3]
l = 1/sigT/n*np.power(10,24)#Mean free path [cm]
print('l: ', l)
#--------------------------------------------------

pE= sigE/sigT
pIE = sigIE/sigT
pA = sigA/sigT


def randPoint():
    #Generates a random direction on the unit sphere, definted by x,y,z.
    longitude = rand.random()*2*PI
    latitude  = math.acos(1-2*rand.random())

    return latitude, longitude

def randomWalk(x,y,z):
    (lat, long) = randPoint()#Gives a random starting direction
    numberScatterings = 0
    
    
    
    x = x+step*l*math.sin(lat)*math.cos(long)
    y =y+step*l*math.sin(lat)*math.sin(long)
    z =z+step*l*math.cos(lat)
    while numberScatterings<6:
        #We take a step of l/4 and randomly decide if the neutron has interacted with an atom or not
        if rand.random()<1-np.power(e, -step):#If the neutron has interacted with an atom
            #print('interact')
            if rand.random()<(pE):
                (lat, long) = randPoint()        
            elif rand.random()<(pIE):
                (lat, long) = randPoint()
                numberScatterings +=1
                #print('Scatt')
        x = x+step*l*math.sin(lat)*math.cos(long)
        y =y+step*l*math.sin(lat)*math.sin(long)
        z =z+step*l*math.cos(lat)
       # xs.append(x)
       # ys.append(y)
       # zs.append(z)
        
    r = np.sqrt(x*x+y*y+z*z)
    return (float(r))
    
rs = []#This will store the final distance from the origin of our nutrons
n=10000
for i in range(n):
    (r) = randomWalk(0,0,0)
    rs.append(r)
  
fig = plt.figure()
ax = fig.add_subplot(111)
ax.hist(rs, bins=60)

