import pygame
import random
import numpy as np
import Config
from ScalarGrid import ScalarGrid



class VectorField(ScalarGrid):
    def __init__(self, rows, columns, colour, origin, gridDirection):
        super().__init__(rows, columns, origin)
        self.colour = colour
        self.origin = origin #measured in real world units
        self.gridDirection = gridDirection

    def drawVectorField(self, screen):
        xOffset = Config.GridOrigin[0] + self.origin[0]*Config.CellVisualSize
        yOffset = Config.GridOrigin[1] + self.origin[1]*Config.CellVisualSize
        cellSize = Config.CellVisualSize

        # cellCenter = cellSize/2
        for jIndex, rowList in enumerate(self.scalarGrid):
            for iIndex, vector in enumerate(rowList):
                vectorStart = (xOffset+cellSize*iIndex, yOffset+cellSize*jIndex)
                vector = [self.gridDirection[0]*vector, self.gridDirection[1]*vector]
                vectorEndX = xOffset+cellSize*iIndex+vector[0]*Config.VectorVisualScale
                vectorEndY = yOffset+cellSize*jIndex+vector[1]*Config.VectorVisualScale
                
                pygame.draw.line(screen, self.colour, vectorStart, (vectorEndX, vectorEndY))
                pygame.draw.circle(screen,self.colour, (vectorEndX, vectorEndY), Config.VectorBallRadius)

    def drawVector(self, screen):
        pass

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

    def calculateVelocityGrid(self, pressureGrid):
        verticalChange = 0
        horizontalChange = 0
        if self.origin[0] == 0:
            horizontalChange = 1
        elif self.origin[1] == 0:
            verticalChange = 1
        preGrid = pressureGrid.scalarGrid
        for j in range(1,self.rows-1):
            for i in range(1,self.columns-1):
                self.scalarGrid[j][i] -= preGrid[j-verticalChange][i-horizontalChange]-preGrid[j][i]

    def bilinearInterpolate(self, coordinates): #coordinate in real world values
        xCoord = coordinates[0] + self.origin[1]/Config.CellSize*1
        yCoord = coordinates[1] + self.origin[0]/Config.CellSize*1
        jIndex = int(coordinates[1]/Config.CellSize)
        iIndex = int(coordinates[0]/Config.CellSize)
        xPercentage = (xCoord-iIndex)
        yPercentage = (yCoord-jIndex)

        NWVelocity = self.scalarGrid[jIndex][iIndex]
        NEVelocity = self.scalarGrid[jIndex][iIndex+1]
        SWVelocity = self.scalarGrid[jIndex+1][iIndex]
        SEVelocity = self.scalarGrid[jIndex+1][iIndex+1]

        topX = (xPercentage/Config.CellSize)*NEVelocity + ((1-xPercentage)/Config.CellSize)*NWVelocity
        bottomX = (xPercentage/Config.CellSize)*SEVelocity + ((1-xPercentage)/Config.CellSize)*SWVelocity

        interpolatedScalar = (yPercentage/Config.CellSize)*bottomX + ((1-yPercentage)/Config.CellSize)*topX
        return interpolatedScalar

    
class VisualVectorField(VectorField):
    def __init__(self, rows, columns, colour, origin, gridDirection):
        super().__init__(rows, columns, colour, origin, gridDirection)
        self.vectorGrid = []

        for x in range(rows): #arranged as a list containing lists of all values in a row
            self.vectorGrid.append([])
            for _ in range(columns):
                self.vectorGrid[x].append([0,0])
    
    def interpolateUpscaledGrid(self, hVectorField, vVectorField):
        for j in range(self.rows-Config.VisualVectorGridUpscaleConstant): 
            for i in range(self.columns-Config.VisualVectorGridUpscaleConstant):

                #calculate real world coordinates of each grid point
                yCoord = j*Config.CellSize/Config.VisualVectorGridUpscaleConstant
                xCoord = i*Config.CellSize/Config.VisualVectorGridUpscaleConstant

                self.vectorGrid[j][i] = [hVectorField.bilinearInterpolate([xCoord,yCoord]), 
                                         vVectorField.bilinearInterpolate([xCoord,yCoord])]
                pass
               
    def drawVectorField(self, screen):
        xOffset = Config.GridOrigin[0] + self.origin[0]*Config.VisualVectorCellSize
        yOffset = Config.GridOrigin[1] + self.origin[1]*Config.VisualVectorCellSize
        cellSize = Config.VisualVectorCellSize

        # cellCenter = cellSize/2
        for jIndex, rowList in enumerate(self.vectorGrid):
            for iIndex, vector in enumerate(rowList):
                vectorStart = (xOffset+cellSize*iIndex, yOffset+cellSize*jIndex)
                vector = [self.gridDirection[0]*vector[0], self.gridDirection[1]*vector[1]]
                vectorEndX = xOffset+cellSize*iIndex+vector[0]*Config.VectorVisualScale
                vectorEndY = yOffset+cellSize*jIndex+vector[1]*Config.VectorVisualScale
                
                pygame.draw.line(screen, self.colour, vectorStart, (vectorEndX, vectorEndY))
                pygame.draw.circle(screen,self.colour, (vectorEndX, vectorEndY), Config.VectorBallRadius)







                

class DivergenceField(ScalarGrid):
    def __init__(self, rows, columns, origin):
        super().__init__(rows, columns, origin)
    
    def calculateDivergence(self, HVectors, VVectors):
        HVectors = HVectors.scalarGrid
        VVectors = VVectors.scalarGrid
        for j in range(self.rows):
            for i in range(self.columns):
                self.scalarGrid[j][i] = (HVectors[j][i]-HVectors[j][i+1]) + (VVectors[j][i]-VVectors[j+1][i])


class CellMap(ScalarGrid):
    def __init__(self, rows, columns, origin): #optimize by creating a list of coordinates containing specific boundary conditions
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
        super().__init__(rows, columns, origin)
    
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
    def __init__(self, rows, columns, origin):
        super().__init__(rows, columns, origin)

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



