import pygame
import random
import numpy as np
import Config
from ScalarGrid import ScalarGrid

class VectorField(ScalarGrid):
    def __init__(self, rows, columns):
        super().__init__(rows, columns)

    
    def drawHorizontalVectorField(self, screen):
        xOffset = Config.GridOrigin[0]
        yOffset = Config.GridOrigin[1]
        cellSize = Config.CellVisualSize
        cellCenter = cellSize/2
        for jIndex, rowList in enumerate(self.scalarGrid):
            for iIndex, vector in enumerate(rowList):
                vectorStart = (xOffset+cellSize*iIndex, yOffset+cellCenter+cellSize*jIndex)
                vectorEndX = xOffset+cellSize*iIndex+vector*Config.VectorVisualScale
                vectorEndY = yOffset+cellCenter+cellSize*jIndex

                pygame.draw.line(screen, Config.RED, vectorStart, (vectorEndX, vectorEndY))
            
                pygame.draw.circle(screen,Config.RED, (vectorEndX, vectorEndY), Config.VectorBallRadius)


    def drawVerticalVectorField(self,screen):
        xOffset = Config.GridOrigin[0]
        yOffset = Config.GridOrigin[1]
        cellSize = Config.CellVisualSize
        cellCenter = cellSize/2
        for jIndex, rowList in enumerate(self.scalarGrid):
            for iIndex, vector in enumerate(rowList):
                vectorStart = (xOffset+cellCenter+cellSize*iIndex, yOffset+cellSize*jIndex)
                vectorEndX = xOffset+cellCenter+cellSize*iIndex
                vectorEndY = yOffset+cellSize*jIndex+vector*Config.VectorVisualScale

                pygame.draw.line(screen, Config.GREEN, vectorStart,(vectorEndX, vectorEndY))
                pygame.draw.circle(screen,Config.GREEN, (vectorEndX, vectorEndY), Config.VectorBallRadius)
    
    def setHorizontalBoundaryConditions(self, cellMap):
        cellMapGrid = cellMap.scalarGrid
        for j in range(cellMap.rows):
            for i in range(cellMap.columns):
                #0 = free flow
                #1 = solid
                #2 = fan
                #3 = void
                if cellMapGrid[j][i] == 1:
                    self.scalarGrid[j][i] = np.float64(0)
                    self.scalarGrid[j][i+1] = np.float64(0)
    
    def setVerticalBoundaryConditions(self, cellMap):
        cellMapGrid = cellMap.scalarGrid
        for j in range(cellMap.rows):
            for i in range(cellMap.columns):
                #0 = free flow
                #1 = solid
                #2 = fan
                #3 = void
                if cellMapGrid[j][i] == 1:
                    self.scalarGrid[j][i] = np.float64(0)
                    self.scalarGrid[j+1][i] = np.float64(0)
                    

    
    def calculateHorizontalVelocityGrid(self, pressureGrid):
        preGrid = pressureGrid.scalarGrid
        for j in range(1,self.rows-1):
            for i in range(1,self.columns-1):
                self.scalarGrid[j][i] -= preGrid[j][i-1]-preGrid[j][i]


    def calculateVerticalVelocityGrid(self, pressureGrid):
        preGrid = pressureGrid.scalarGrid
        for j in range(1,self.rows-1):
            for i in range(1,self.columns-1):
                self.scalarGrid[j][i] -= preGrid[j-1][i]-preGrid[j][i]


                

class DivergenceField(ScalarGrid):
    def __init__(self, rows, columns):
        super().__init__(rows, columns)
    
    def calculateDivergence(self, HVectors, VVectors):
        HVectors = HVectors.scalarGrid
        VVectors = VVectors.scalarGrid
        for j in range(self.rows):
            for i in range(self.columns):
                self.scalarGrid[j][i] = (HVectors[j][i]-HVectors[j][i+1]) + (VVectors[j][i]-VVectors[j+1][i])


class CellMap(ScalarGrid):
    def __init__(self, rows, columns): #optimize by creating a list of coordinates containing specific boundary conditions
        # self.rows = rows
        # self.columns = columns
        # self.scalarGrid = []

        #0 = free flow
        #1 = solid
        #2 = fan
        #3 = void
        
        # for x in range(rows): #arranged as a list containing lists of all values in a row
        #     self.scalarGrid.append([])
        #     for _ in range(columns):
        #         pass
        #         # self.scalarGrid[x].append(np.float64(0))
        super().__init__(rows, columns)
    
    def setWallSolid(self, wallDirection):
        match wallDirection:
            case "north":
                for i in range(self.columns):
                # for j in range(self.rows):
                #     for i in range(self.columns):
                        self.scalarGrid[0][i] = np.float64(1)
            case "east":
                for j in range(self.rows):
                # for j in range(self.rows):
                #     for i in range(self.columns):
                        self.scalarGrid[j][self.columns-1] = np.float64(1)
            case "south":
                for i in range(self.columns):
                # for j in range(self.rows):
                #     for i in range(self.columns):
                        self.scalarGrid[self.rows-1][i] = np.float64(1)
            case "west":
                for j in range(self.rows):
                # for j in range(self.rows):
                #     for i in range(self.columns):
                        self.scalarGrid[j][0] = np.float64(1)


    def setWallFan(self, wallDirection):
        pass

    def setWallVoid(self, wallDirection):
        pass



class PressureField(ScalarGrid):
    def __init__(self, rows, columns):
        super().__init__(rows, columns)

    # def resetBoundaryConditions(self, cellMap):
    #     cellMap = cellMap.scalarGrid
    #     for j in range(self.rows):
    #         for i in range(self.columns):
    #             if cellMap[j][i] == 1:


    def GaussSeidelLoop(self, divGrid, cellMap):
        for _ in range (Config.GaussSeidelIterations):
            self.calculatePressureGrid(divGrid, cellMap)

    def calculatePressureGrid(self, divGrid, cellMap):
        divGrid = divGrid.scalarGrid
        for j in range(1,self.rows-1):
            for i in range(1,self.columns-1):
                right = self.findNeighbourPressureValue(j, i, [0,1], cellMap)
                left = self.findNeighbourPressureValue(j,i,[0,-1],cellMap)
                top = self.findNeighbourPressureValue(j,i,[-1,0],cellMap)
                bottom = self.findNeighbourPressureValue(j,i,[1,0],cellMap)

                self.scalarGrid[j][i] = (right + left + top + bottom - divGrid[j][i])/4

    def findNeighbourPressureValue(self, j, i, direction, cellMap):
        cellMap = cellMap.scalarGrid
        originJ = j
        originI = i
        j += direction[0]
        i += direction[1]
        # for Ydirection in (-1,1):
        #     j = originJ + Ydirection
        #     for Xdirection in (-1,1):
        #         i = originI + Xdirection

            #0 = free flow
            #1 = solid
            #2 = fan
            #3 = void
        if cellMap[j][i] == 0:
            return self.scalarGrid[j][i]
        elif cellMap[j][i] == 1 or cellMap[j][i] == 2:
            return self.scalarGrid[originJ][originI] #use Pc pressure
        # elif cellMap[j][i] == 2:
        #     return self.scalarGrid[originJ][originI]
        elif cellMap[j][i] == 3:
            return 0



