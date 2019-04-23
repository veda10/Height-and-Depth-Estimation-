import cv2
import scipy.misc
import numpy as np
import matplotlib.pyplot as plt
import warnings
import math

def intersection_points(a1,a2,b1,b2):
	""" 
    Returns the point of intersection of the lines passing through a2,a1 and b2,b1.
    a1: [x, y] a point on the first line
    a2: [x, y] another point on the first line
    b1: [x, y] a point on the second line
    b2: [x, y] another point on the second line
    """
	s = np.vstack([a1,a2,b1,b2])        # s for stacked
	h = np.hstack((s, np.ones((4, 1)))) # h for homogeneous
	l1 = np.cross(h[0], h[1])           # get first line
	l2 = np.cross(h[2], h[3])           # get second line
	x, y, z = np.cross(l1, l2)          # point of intersection
	if z == 0:                          # lines are parallel
		return (float('inf'), float('inf'))
	return (x/z, y/z)

def distance(A1,A2):
	return math.sqrt((A1[0]-A2[0])**2 + (A1[1]-A2[1])**2)

	
#Reading Image
image_path = 'img.jpg'
image = cv2.imread(image_path,1)
plt.imshow(image)

#pole inputs
pole = plt.ginput(2)
pole_up = pole[0]
pole_down = pole[1]
#print(pole)
plt.plot([pole_up[0],pole_down[0]],[pole_up[1],pole_down[1]],marker = 'o')

#Tractor inputs
tractor = plt.ginput(2)
tractor_up = tractor[0]
tractor_down = tractor[1]
#print(tractor)
plt.plot([tractor_up[0],tractor_down[0]],[tractor_up[1],tractor_down[1]],marker = 'o')

#Building inputs
building = plt.ginput(2)
building_up = building[0]
building_down = building[1]
#print(building)
plt.plot([building_up[0],building_down[0]],[building_up[1],building_down[1]],marker = 'o')



#vanishing points
vanish_lines = 4
vanish_points = 2*vanish_lines
vanishing = plt.ginput(vanish_points)
vanishing_points=[]
for i in range(0,vanish_points,vanish_lines):
	A1 = vanishing[i]
	A2 = vanishing[i+1]
	B1 = vanishing[i+2]
	B2 = vanishing[i+3]
	
	plt.plot([A1[0], A2[0]], [A1[1], A2[1]], marker = 'o')
	plt.plot([B1[0], B2[0]], [B1[1], B2[1]], marker = 'o')
	p1,p2 = intersection_points(A1,A2,B1,B2)
	#print(p1)
	#print(p2)
	vanishing_points.append((p1,p2))
#print(vanishing_points)
#plot the vanishing_points
plt.plot([vanishing_points[0][0], vanishing_points[1][0]], [vanishing_points[0][1], vanishing_points[1][1]], marker = 'o')


#Line Equation - Tractor bottom,pole bottom
P1 = pole_down
P2 = tractor_down
V1 = vanishing_points[0]
V2 = vanishing_points[1]
point_on_vanishLine = intersection_points(P1,P2,V1,V2)

plt.plot([tractor_down[0],point_on_vanishLine[0]],[tractor_down[1],point_on_vanishLine[1]], marker = 'o')
plt.plot([tractor_up[0],point_on_vanishLine[0]],[tractor_up[1],point_on_vanishLine[1]], marker = 'o')

#print(point_on_vanishLine)

P1 = pole_up
P2 = pole_down
V1 = tractor_up
V2 = point_on_vanishLine

Tractor_reference = intersection_points(P1,P2,V1,V2)
pole_height = 1.65

#tractor_height = pole_height*(np.linalg.norm(np.array(Tractor_reference))-np.array(pole_down))*1.0/(np.linalg.norm(np.array(pole_up))-np.array(pole_down)) 
tractor_height = pole_height*(distance(Tractor_reference,pole_down))*1.0/distance(pole_up,pole_down)

print(pole_height)
print("Tractor-height:",tractor_height,end=" ")

#########################################Building Height###############################################
P1 = pole_down
P2 = building_down
V1 = vanishing_points[0]
V2 = vanishing_points[1]
point_on_vanishLine = intersection_points(P1,P2,V1,V2)

plt.plot([building_down[0],point_on_vanishLine[0]],[building_down[1],point_on_vanishLine[1]], marker = 'o')
plt.plot([building_up[0],point_on_vanishLine[0]],[building_up[1],point_on_vanishLine[1]], marker = 'o')

#print(point_on_vanishLine)

P1 = pole_up
P2 = pole_down
V1 = building_up
V2 = point_on_vanishLine

Building_reference = intersection_points(P1,P2,V1,V2)
pole_height = 1.65

#Building_height = pole_height*(np.linalg.norm(np.array(Building_reference).T)-np.array(pole_down).T)*1.0/(np.linalg.norm(np.array(pole_up).T)-np.array(pole_down).T) 

Building_height = pole_height*(distance(Building_reference,pole_down))*1.0/distance(pole_up,pole_down)

print(pole_height)
print("Building Height:")
print(Building_height)

####################################CAMERA HEIGHT##########################################################################################
P1 = pole_down
P2 = pole_up
V1 = vanishing_points[0]
V2 = vanishing_points[1]
point_on_vanishLine = intersection_points(P1,P2,V1,V2)

"""
plt.plot([building_down[0],point_on_vanishLine[0]],[building_down[1],point_on_vanishLine[1]], marker = 'o')
plt.plot([building_up[0],point_on_vanishLine[0]],[building_up[1],point_on_vanishLine[1]], marker = 'o')

#print(point_on_vanishLine)

P1 = pole_up
P2 = pole_down
V1 = building_up
V2 = point_on_vanishLine

Building_reference = intersection_points(P1,P2,V1,V2)
"""
pole_height = 1.65

#Building_height = pole_height*(np.linalg.norm(np.array(Building_reference).T)-np.array(pole_down).T)*1.0/(np.linalg.norm(np.array(pole_up).T)-np.array(pole_down).T) 

Camera_height = pole_height*(distance(point_on_vanishLine,pole_down))*1.0/distance(pole_up,pole_down)

print(pole_height)
print("Camera Height:")
print(Camera_height)




plt.show()















