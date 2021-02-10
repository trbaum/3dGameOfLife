#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 18:14:39 2021

@author: teddyrosenbaum
"""
import numpy as np

class vector:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
        
    def dot(self,v):
        """
        Description
        --------
        Finds the dot product of vector and v 
        
        Input
        ----
        Vector v
        
        Output
        ----
        Double
        
        """ 
        return self.x * v.x + self.y * v.y + self.z * v.z
    
    def cross(self, v):
        """
        Description
        --------
        Finds the cross product of vector and v 
        
        Input
        ----
        Vector v
        
        Output
        ----
        Vector
        
        """ 
        return vector((self.y*v.z)-(v.y*self.z),-(self.x*v.z)+(v.x*self.z),(self.x*v.y)-(v.x*self.y))
    
    def mag(self):
        """
        Description
        --------
        Finds magnitude of vector
        
        Input
        ----
        Vector v
        
        Output
        ----
        Double
        
        """ 
        return ((self.x**2) + (self.y**2) + (self.z**2))**(1/2)
    
    def angle(self, v):
        """
        Description
        --------
        Finds the angle between vector and v in degrees
        
        Input
        ----
        Vector v
        
        Output
        ----
        Double
        
        """ 
        return 180 / np.pi * np.arccos(self.dot(v)/self.mag()/v.mag())
    
    def normalize(self):
        """
        Description
        --------
        Normalizes vector
        
        Input
        ----
        None
        
        Output
        ----
        Vector
        
        """ 
        k = self.mag()
        self.x = self.x / k
        self.y = self.y / k
        self.z = self.z / k
        return self

class point:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
    

class line:
    def __init__(self,kx,ky,kz,slopex,slopey,slopez):
        self.k = vector(kx,ky,kz)
        self.s = vector(slopex,slopey,slopez)
 
def pointToLine(p1,p2):
    """
    Description
    --------
    Returns a line between p1 and p2
    
    Input
    ----
    Point p1
    Point p2
    
    Output
    ----
    Line
    
    """ 
    return line(p1.x,p1.y,p1.z,p1.x-p2.x,p1.y-p2.y,p1.z-p2.z)     
 
class plane:
    def __init__(self,k,ox,oy,oz):
        self.k = k
        self.o = vector(ox,oy,oz)
        

def pointPointDistance(p1,p2):
    """
    Description
    --------
    Finds the distance between p1 and p2
    
    Input
    ----
    Point p1
    Point p2
    
    Output
    ----
    Double
        
    """ 
    return ((p1.x-p2.x)**2 + (p1.y-p2.y)**2 + (p1.z-p2.z)**2) ** (1/2)

def pointLineDistance(line,point):
    """
    Description
    --------
    Finds the minimum distance between a line and point
    
    Input
    ----
    Line line
    Point point
    
    Output
    ----
    Double
        
    """ 
    l = line.s.x*point.x + line.s.y*point.y + line.s.z*point.z
    p = plane(l,line.s.x,line.s.y,line.s.z)
    return pointPointDistance(point,planeLineIntersect(line,p))

def planeLineIntersect(line,plane):
    """
    Description
    --------
    Finds the intersect between a line and a plane
    Returns intersect or False if they do not intersect or line is in plane
    
    Input
    ----
    Line line
    Plane plane
        
    Output
    ----
    Point or Boolean
        
    """ 
    if plane.o.dot(line.s) == 0:
        return False
    i = (plane.k - (line.k.x * plane.o.x) - (line.k.y * plane.o.y) - (line.k.z * plane.o.z))/((line.s.x * plane.o.x) + (line.s.y * plane.o.y) + (line.s.z * plane.o.z))
    return point((line.s.x * i) + line.k.x, (line.s.y * i) + line.k.y, (line.s.z * i) + line.k.z)

def segmentIntersects(p1,p2,p3,p4):
    """
    Description
    --------
    Finds the intersection between segment bound by p1 and p2 and segment bound by p3 and p4
    Returns intersect or False if they do not intersect 
    
    Input
    ----
    Point p1
    Point p2
    Point p3
    Point p4
        
    Output
    ----
    Point or Boolean
        
    """ 
    l1 = pointToLine(p1, p2)
    l2 = pointToLine(p3, p4) 
    p = lineLineIntersect(l1, l2)
    if(p == False):
        return False
    else:
        try:
            if(between(p1, p2, p) and between(p3, p4, p)):
                return True
        except:
            print(p1)
            print(p2)
            print(p3)
            print(p4)
            print(p)
    return False
    
def lineLineIntersect(l1,l2):
    """
    Description
    --------
    Finds the intersect between a lines
    Returns intersect or False if they do not intersect
    
    Input
    ----
    Line l1
    Line l2
        
    Output
    ----
    Point or Boolean
        
    """ 
    if(parralell(l1, l2)):
        return False

    v = l1.s.cross(l2.s)
    if(v.x*l1.k.x + v.y*l1.k.y + v.z*l1.k.z  == v.x*l2.k.x + v.y*l2.k.y + v.z*l2.k.z): #checks if lines are coplaner
        i = 0
        j = 0
        if (l2.s.y * l1.s.x) - (l1.s.y * l2.s.x) != 0:
            i = ((l1.k.y * l2.s.x) - (l2.k.y * l2.s.x) + (l2.k.x * l2.s.y) - (l1.k.x * l2.s.y))/((l2.s.y * l1.s.x) - (l1.s.y * l2.s.x))
        else:    
            if (l2.s.z * l1.s.x) - (l1.s.z * l2.s.x) != 0:
                i = ((l1.k.z * l2.s.x) - (l2.k.z * l2.s.x) + (l2.k.x * l2.s.z) - (l1.k.x * l2.s.z))/((l2.s.z * l1.s.x) - (l1.s.z * l2.s.x))
            else:
                i = ((l1.k.y * l2.s.z) - (l2.k.y * l2.s.z) + (l2.k.z * l2.s.y) - (l1.k.z * l2.s.y))/((l2.s.y * l1.s.z) - (l1.s.y * l2.s.z))
        if(l2.s.x != 0):
            j = ((l1.s.x * i) + l1.k.x - l2.k.x) / l2.s.x
        else:
            if(l2.s.y != 0):
                j = ((l1.s.y * i) + l1.k.y - l2.k.y) / l2.s.y
            else:
                j = ((l1.s.z * i) + l1.k.z - l2.k.z) / l2.s.z
                
    
        if(l1.s.z * i + l1.k.z == l2.s.z * j + l2.k.z):
            #return point(np.round(l1.s.x * i + l1.k.x,decimals=5),np.round(l1.s.y * i + l1.k.y,decimals=5),np.round(l1.s.z * i + l1.k.z,decimals=5))
            return point(l1.s.x * i + l1.k.x,l1.s.y * i + l1.k.y,l1.s.z * i + l1.k.z)
            
    return False

def parralell(l1,l2):
    """
    Description
    --------
    Determines if two lines are parralell
    
    Input
    ----
    Line l1
    Line l2
        
    Output
    ----
    Boolean
        
    """ 
    ratio = 0
    if(l1.s.x != 0 and l2.s.x != 0):
        ratio = l2.s.x / l1.s.x
        if(ratio * l1.s.y == l2.s.y and ratio * l1.s.z == l2.s.z):
            return True
    if(l1.s.y != 0 and l2.s.y != 0):
        ratio = l2.s.y / l1.s.y
        if(ratio * l1.s.x == l2.s.x and ratio * l1.s.z == l2.s.z):
            return True
    if(l1.s.z != 0 and l2.s.z != 0):
        ratio = l2.s.z / l1.s.z
        if(ratio * l1.s.y == l2.s.y and ratio * l1.s.x == l2.s.x):
            return True
    if(ratio == 0):
        return False
        
    

def between(p1,p2,p3):
    """
    Description
    --------
    Determines if p3 is in rectangle bound by p1 and p2 
    If 1 parameter is the same ignores it to deal with rounding error
    
    Input
    ----
    Line line
    Plane plane
        
    Output
    ----
    Point or Boolean
        
    """ 
    
    if(p1.x == p2.x):
        
        if((p1.y >= p3.y and p3.y >= p2.y) or (p2.y >= p3.y and p3.y >= p1.y)):
            if((p1.z >= p3.z and p3.z >= p2.z) or (p2.z >= p3.z and p3.z >= p1.z)):
                return True
    
    if(p1.y == p2.y):
        if((p1.x >= p3.x and p3.x >= p2.x) or (p2.x >= p3.x and p3.x >= p1.x)):
            if((p1.z >= p3.z and p3.z >= p2.z) or (p2.z >= p3.z and p3.z >= p1.z)):
                return True

    if(p1.z == p2.z):
        if((p1.y >= p3.y and p3.y >= p2.y) or (p2.y >= p3.y and p3.y >= p1.y)):
            if((p1.x >= p3.x and p3.x >= p2.x) or (p2.x >= p3.x and p3.x >= p1.x)):
                return True
    if((p1.x >= p3.x and p3.x >= p2.x) or (p2.x >= p3.x and p3.x >= p1.x)):
        if((p1.y >= p3.y and p3.y >= p2.y) or (p2.y >= p3.y and p3.y >= p1.y)):
            if((p1.z >= p3.z and p3.z >= p2.z) or (p2.z >= p3.z and p3.z >= p1.z)):
                return True
    return False


    
    
    
    
    
    
    