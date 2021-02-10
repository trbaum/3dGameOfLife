#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 17:52:51 2021

@author: teddyrosenbaum
"""

import py3d as td

def test():
    b = board(3)
    b.makeCell(0,2,0)
    b.makeCell(1,1,1)
    b.makeCell(2,0,2)
    b.render(0)

class board:
    def __init__(self, size, rules = [3,8,5,6]):
        self.board = makeBoard(size)
        self.size = size
        self.rules = rules
        self.w = td.workSpace()
        self.w.cameras.append(td.camera(30,30,50,50,.5,-5,2,-7,90))
        self.w.lights.append(td.light(5,-1,-1,1))
        
    def makeCell(self, x, y, z):
        """
        Description
        --------
        Sets the Cell at x, y, z to alive
        
        Input
        ----
        Ints x, y, z
        
        Output
        ----
        None
        
        """

        self.board[x][y][z] = True
        
    def neighbors(self, x, y, z):
        """
        Description
        --------
        Returns the number of neigbors around the cell at x, y, z
        
        Input
        ----
        Ints x, y, z
        
        Output
        ----
        Int number of neighbors
        
        """

        tot = 0
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    if(i != 1 and j != 1 and k != 1):
                        if(i+x > 0 and i+x < self.size and j+y > 0 and j+y < self.size and k+z > 0 and k+z < self.size):
                            if(self.board[x+i-1][y+j-1][z+k-1] == True):
                                tot += 1
                                
    def update(self):
        """
        Description
        --------
        Updates the board following the given rules
        
        Input
        ----
        None
        
        Output
        ----
        None
        
        """

        newBoard = makeBoard(self.size)
        for i in range(self.size):
            for j in range(self.size):
                for k in range(self.size):
                    tot = self.neighbors(i,j,k)
                    if(tot <= self.rules[0] and tot >= self.rules[1] and self.board[i][j][k] == True):
                        newBoard[i][j][k] = True
                    if(tot <= self.rules[2] and tot >= self.rules[3]):
                        newBoard[i][j][k] = True
        self.board = newBoard
        
    def render(self,index=0):
        """
        Description
        --------
        Creates a 3d image of the board
        
        Input
        ----
        None
        
        Output
        ----
        None
        
        """
        self.w.surfaces = []
        for i in range(self.size):
            for j in range(self.size):
                for k in range(self.size):
                    self.w.addCube(i/self.size, j/self.size, 1 - k/self.size, 1/self.size)

        self.w.renderCamera(index)

        
def makeBoard(size):
    """
    Description
    --------
    Creates a 3d array of booleans with lenght size
    True indicating a cell is alive  
    False indicating that it is dead
    
    Input
    ----
    Int size
    
    Output
    ----
    Boolean[][][]
        
    """
    return [[[False] * size] * size] * size

