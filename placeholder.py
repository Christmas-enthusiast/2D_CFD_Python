#a placeholder file to rewrite vectorField class
# The goal of this rewrite is so the class will revolve around real world coordinates, 
# then all calculations such as calculating the offset when drawing is automated 
# and so is calculating bilinear interpolations
import Config
import pygame
from ScalarGrid import ScalarGrid
import numpy as np

class VectorField(ScalarGrid):
    def __init__(self, rows, columns, origin):
        super().__init__(rows, columns)
        self.origin = origin #measured in real world units
    
    def drawVectorField(self, screen):
        xOffset = Config.GridOrigin[0] + self.origin[0]
        yOffset = Config.GridOrigin[1] + self.origin[1]
        cellSize = Config.CellVisualSize
        # cellCenter = cellSize/2
        for jIndex, rowList in enumerate(self.scalarGrid):
            for iIndex, vector in enumerate(rowList):
                vectorStart = (xOffset+cellSize*iIndex, yOffset+cellSize*jIndex)
                vectorEndX = xOffset+cellSize*iIndex+vector*Config.VectorVisualScale
                vectorEndY = yOffset+cellSize*jIndex

                pygame.draw.line(screen, Config.RED, vectorStart, (vectorEndX, vectorEndY))
            
                pygame.draw.circle(screen,Config.RED, (vectorEndX, vectorEndY), Config.VectorBallRadius)

    # def drawVerticalVectorField(self,screen):
    #     xOffset = Config.GridOrigin[0]
    #     yOffset = Config.GridOrigin[1]
    #     cellSize = Config.CellVisualSize
    #     cellCenter = cellSize/2
    #     for jIndex, rowList in enumerate(self.scalarGrid):
    #         for iIndex, vector in enumerate(rowList):
    #             vectorStart = (xOffset+cellCenter+cellSize*iIndex, yOffset+cellSize*jIndex)
    #             vectorEndX = xOffset+cellCenter+cellSize*iIndex
    #             vectorEndY = yOffset+cellSize*jIndex+vector*Config.VectorVisualScale

    #             pygame.draw.line(screen, Config.GREEN, vectorStart,(vectorEndX, vectorEndY))
    #             pygame.draw.circle(screen,Config.GREEN, (vectorEndX, vectorEndY), Config.VectorBallRadius)
    
    def setBoundaryConditions(self, cellMap):
        verticalChange = 0
        horizontalChange = 0
        if self.origin[0] == 0:
            horizontalChange = 1
        elif self.origin[1] == 0:
            verticalChange = 1
        cellMapGrid = cellMap.scalarGrid
        for j in range(cellMap.rows):
            for i in range(cellMap.columns):
                #0 = free flow
                #1 = solid
                #2 = fan
                #3 = void
                if cellMapGrid[j][i] == 1:
                    self.scalarGrid[j][i] = np.float64(0)
                    self.scalarGrid[j+verticalChange][i+horizontalChange] = np.float64(0)
    
    # def setVerticalBoundaryConditions(self, cellMap):
    #     cellMapGrid = cellMap.scalarGrid
    #     for j in range(cellMap.rows):
    #         for i in range(cellMap.columns):
    #             #0 = free flow
    #             #1 = solid
    #             #2 = fan
    #             #3 = void
    #             if cellMapGrid[j][i] == 1:
    #                 self.scalarGrid[j][i] = np.float64(0)
    #                 self.scalarGrid[j+1][i] = np.float64(0)
    
    def calculateVelocityGrid(self, pressureGrid):
        preGrid = pressureGrid.scalarGrid
        for j in range(1,self.rows-1):
            for i in range(1,self.columns-1):
                self.scalarGrid[j][i] -= preGrid[j-1][i]-preGrid[j][i]


    # def calculateHorizontalVelocityGrid(self, pressureGrid):
    #     preGrid = pressureGrid.scalarGrid
    #     for j in range(1,self.rows-1):
    #         for i in range(1,self.columns-1):
    #             self.scalarGrid[j][i] -= preGrid[j][i-1]-preGrid[j][i]

    # def calculateVerticalVelocityGrid(self, pressureGrid):
    #     preGrid = pressureGrid.scalarGrid
    #     for j in range(1,self.rows-1):
    #         for i in range(1,self.columns-1):
    #             self.scalarGrid[j][i] -= preGrid[j-1][i]-preGrid[j][i]

