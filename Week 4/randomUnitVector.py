import random as rand
import matplotlib.pyplot as plt
import math
from mpl_toolkits.mplot3d import Axes3D
PI = 3.1415926535

def randPoint():
    #Generates a random point on the unit sphere, definted by x,y,z.
    longitude = rand.random()*2*PI
    latitude  = math.acos(1-2*rand.random())
    
    x = math.sin(latitude)*math.cos(longitude)
    y = math.sin(latitude)*math.sin(longitude)
    z = math.cos(latitude)

    
    return x,y,z
x = []
y = []
z = []
for i in range(1, 10000):
    (a,b,c) = randPoint()
    x.append(a)
    y.append(b)
    z.append(c)
    

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(x,y,z, s=1)