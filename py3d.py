#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 16:55:09 2021

need to get colors and shadows working
fix holes in surfaces

@author: teddyrosenbaum
"""
import numpy as np
import py3dMath as mp
import matplotlib.pyplot as plt

def test():
    """
    Description
    --------
    Makes and displays a 3d cube 
    
    Input
    ----
    None
    
    Output
    ----
    None
        
    """
    w = workSpace()
    w.cameras.append(camera(30,30,100,100,-3,-3,2,-15,45))
    w.lights.append(light(10,-3,-3,2))
    w.addCube(0,0,0,1)
    w.renderCamera(0)

def makeColor(brightness,color):
    """
    Description
    --------
    Makes a shade of a color given a brightness value and a color
    
    Input
    ----
    Double brightness
    Double[] color with RGB color values
    
    Output
    ----
    Double[] with RGB color values
        
    """
    maxBrightness = 10
    c = []
    if(brightness >= maxBrightness):
        return [1,1,1]
    for i in color:
        c.append((1/(maxBrightness-brightness) * i) / (1/(maxBrightness-brightness) + 1/(brightness))) #weighted mean with color and black
    return c

    
def brightness(surface,lights,camera,x,y,z):
        """
        Description
        --------
        Returns the brightness value based no relitive angle and distance from all the lights
        
        Input
        ----
        Surface surface 
        Light[] lights
        Camera camera
        Doubles x, y, z 
        
        Output
        ----
        Double 
            
        """
        brightness = 1
        v1 = surface.plane.o
        v2 = mp.vector(camera.x - x, camera.y - y, camera.z - z)
        if v1.angle(v2) > 90:
            v1.x = -v1.x
            v1.y = -v1.y
            v1.z = -v1.z
        for i in lights:
            v3 = mp.vector(i.x - x, i.y - y, i.z - z)
            d = mp.pointPointDistance(mp.point(i.x,i.y,i.z),mp.point(x,y,z))
            brightness = brightness + (np.sin(np.pi / 180 * v1.angle(v3)) * i.brightness /(4 * np.pi * d * d))
        return brightness

    
class workSpace:
    def __init__(self):
        self.cameras = []
        self.lights = []
        self.surfaces = []
        
    def clearSurfaces(self):
        """
        Description
        --------
        Removes any surfaces from workSpace
        
        Input
        ----
        None
        
        Output
        ----
        None
            
        """
        self.surfaces = []
    
    def renderCamera(self,camIndex):
        """
        Description
        --------
        Creates a 3d image from perspective of camera at index camIndex
        
        Input
        ----
        Int camIndex
        
        Output
        ----
        None
            
        """
        camera = self.cameras[camIndex]
        ax = plt.gca()
        c = mp.point(camera.x,camera.y,camera.z)
        
        for i in range(camera.pixX):
            for j in range(camera.pixY):
                yaw = ((camera.yaw-camera.angleX/2) + ((camera.angleX * (camera.pixX - i))/camera.pixX)) * np.pi / 180
                pitch = ((camera.pitch-camera.angleY/2) + ((camera.angleY * (j)/camera.pixY))) * np.pi / 180
                l = mp.line(c.x, c.y, c.z, np.cos(yaw), np.sin(yaw), np.tan(pitch))        
                point = []
                index = []
                for k in range(len(self.surfaces)):
                    surface = self.surfaces[k]
                    p = mp.planeLineIntersect(l,surface.plane)
                    if(p != False):
                        if(surface.inSurface(p)):
                            point.append(p)
                            index.append(k)
                    '''old could reduce computational demand
                    if(mp.pointLineDistance(l,surface.center) <= surface.radius):
                        p = mp.planeLineIntersect(l,self.surface.plane)
                        if(self.surfaces[k].inSurface(p)):
                            point.append(p)
                            index.append(i)
                    '''
                
                if(len(point) == 0):
                    ax.add_patch(plt.Rectangle([i,j], 1, 1, color = [1,1,1]))
                    
                else:
                    
                    minVal = mp.pointPointDistance(c,point[0])
                    minValIndex = 0
                    for k in range(len(point)):
                        distance  = mp.pointPointDistance(c,point[k])
                        if(minVal >= distance):
                            minVal = distance
                            minValIndex = k
                    #need to add lines to light to add shadows
                    surface = self.surfaces[index[minValIndex]]
                    #b = brightness(surface,self.lights,camera,point[minValIndex].x,point[minValIndex].y,point[minValIndex].z)
                    #ax.add_patch(makePixel(i,j,b,self.surfaces[minValIndex].color))
                    ax.add_patch(plt.Rectangle([i,j], 1, 1, color = [0,0,0]))
        plt.axis('scaled')
        plt.axis('off')
        plt.show()
        
        
    
    def addCube(self,x,y,z,size):
        """
        Description
        --------
        Adds a cube at location x, y, z with a size of size
        
        Input
        ----
        Doubles x, y, z
        Double size
        
        Output
        ----
        None
            
        """
        p1 = mp.point(x,y,z)
        p2 = mp.point(x+size,y,z)
        p3 = mp.point(x,y+size,z)
        p4 = mp.point(x,y,z+size)
        p5 = mp.point(x+size,y+size,z)
        p6 = mp.point(x+size,y,z+size)
        p7 = mp.point(x,y+size,z+size)
        p8 = mp.point(x+size,y+size,z+size)
        self.surfaces.append(surface([0,0,0],[p1,p2,p5,p3])) #z constant
        self.surfaces.append(surface([0,0,0],[p4,p6,p8,p7])) #z constant
        self.surfaces.append(surface([0,0,0],[p1,p2,p6,p4])) #y constant
        self.surfaces.append(surface([0,0,0],[p3,p5,p8,p7])) #y constant
        self.surfaces.append(surface([0,0,0],[p1,p3,p7,p4])) #x constant
        self.surfaces.append(surface([0,0,0],[p2,p5,p8,p6])) #x constant
       

class light:
    def __init__(self,brightness,x,y,z):
        self.brightness = brightness
        self.x = x
        self.y = y
        self.z = z
        

class camera:
    def __init__(self,angleX,angleY,pixX,pixY,x,y,z,pitch,yaw):
        self.angleX = angleX
        self.angleY = angleY
        self.pixX = pixX
        self.pixY = pixY
        self.x = x
        self.y = y
        self.z = z
        self.pitch = pitch
        self.yaw = yaw
        

class surface:
    #all points must be in same plane
    def __init__(self,color,points):
        self.color = color
        self.points = points
        v1 = mp.vector(self.points[1].x - self.points[0].x, self.points[1].y - self.points[0].y, self.points[1].z - self.points[0].z)
        v2 = mp.vector(self.points[1].x - self.points[2].x, self.points[1].y - self.points[2].y, self.points[1].z - self.points[2].z)
        v3 = v1.cross(v2)  
        self.plane = mp.plane(v3.x*self.points[0].x+v3.y*self.points[0].y+v3.z*self.points[0].z,v3.x,v3.y,v3.z)
        self.radius = 0 
        self.c = self.center()
        for p in self.points:
            d = mp.pointPointDistance(p,self.c)
            if d > self.radius:
                self.radius = d
         
        
    '''
    def add(self,x,y,z):
        self.x.append(x)
        self.y.append(y)
        self.z.append(z)
    '''
    
    def center(self):
        """
        Description
        --------
        Finds the center of surface 
        
        Input
        ----
        None
        
        Output
        ----
        Point
        
        """   
        xtot = 0
        ytot = 0
        ztot = 0
        for i in self.points:
            xtot = xtot + i.x
            ytot = ytot + i.y
            ztot = ztot + i.z
        return mp.point(xtot/len(self.points),ytot/len(self.points),ztot/len(self.points))
    
    def inSurface(self,p):
        """
        Description
        --------
        Determines if point p is in surface
        Returns True if it is otherwise returns False
        
        Input
        ----
        Point p
        
        Output
        ----
        Boolean 
        
        """ 
        tot = 0
        
        sx = self.points[0].x-self.points[1].x
        sy = self.points[0].y-self.points[1].y
        sz = self.points[0].z-self.points[1].z
        k = (100 * mp.vector(sx,sy,sz).mag())
        p1 = mp.point(p.x+(sx*k*self.radius),p.y+(sy*k*self.radius),p.z+(sz*k*self.radius))
        for i in range(len(self.points)-2):
            if mp.segmentIntersects(p,p1,self.points[i],self.points[i+1]):
                tot = tot + 1
        if mp.segmentIntersects(p,p1,self.points[0],self.points[-1]):
            tot = tot + 1
        '''
        for i in range(len(self.points)-1):
            p1 = self.points[i]
            p2 = self.points[i+1]
            intersect = mp.segmentIntersects(p,self.c,p1,p2)
            if intersect:
                tot = tot + 1

        p1 = self.points[0]
        p2 = self.points[-1]
        intersect = mp.segmentIntersects(p,self.c,p1,p2)
        if intersect:
            tot = tot + 1

        '''
        
        if tot%2 == 1:
            return True
        return False

