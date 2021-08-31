#Produces a random sample of points in an exponential format

import matplotlib.pyplot as plt
import numpy as np
import random as rand

l = 45
points = []
logPoints = []

for i in range(999999):
    point = -l*np.log(rand.random())
    points.append(point)
    
    
fig = plt.figure()
ax = plt.subplot(111)
ax1 = plt.subplot(111)
ax.hist(points, bins = 100, log = True)
plt.show()

n150 = 0
n0 = 0
for point in points:
    if point>=150 and point<156:
        n150+=1
    if point<6:
        n0+=1
        
grad = (np.log(n150)-np.log(n0))/153
print(grad)
#ax1.scatter()

#for point in points:
    