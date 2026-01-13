import pygame
import random
import numpy as np
import Config
from ScalarGrid import ScalarGrid

class VectorFieldNew():
    def __init__(self, rows, columns, colour, origin=[0,0]):
        for x in range(rows): #arranged as a list containing lists of all values in a row
            self.scalarGrid.append([])
            for _ in range(columns):
                self.scalarGrid[x].append(np.float64(0))

class VectorField(ScalarGrid):
    def __init__(self, rows, columns, colour, origin, gridDirection):
        super().__init__(rows, columns, origin)
        self.colour = colour
        self.origin = origin #measured in real world units
        self.gridDirection = gridDirection
    
    def setZero(self):
        for j in range(self.rows):
            for i in range(self.columns):
                self.scalarGrid[j][i] = np.float64(0)

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
                
                self.drawVector(screen, vectorStart, (vectorEndX,vectorEndY), drawTail=True)
                # pygame.draw.line(screen, self.colour, vectorStart, (vectorEndX, vectorEndY))
                # pygame.draw.circle(screen,self.colour, (vectorEndX, vectorEndY), Config.VectorBallRadius)

    def drawVector(self, screen, vectorStart, vectorEnd, drawBall=True, drawTail=True):
        if drawTail:
            pygame.draw.line(screen, self.colour, vectorStart, vectorEnd)
        if drawBall:
            pygame.draw.circle(screen, self.colour, vectorEnd, Config.VectorBallRadius)

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
        # verticalChange = 0
        # horizontalChange = 0
        # if self.origin[0] == 0:
        #     horizontalChange = 1
        # elif self.origin[1] == 0:
        #     verticalChange = 1

        preGrid = pressureGrid.scalarGrid
        for j in range(1,self.rows-1):
            for i in range(1,self.columns-1):
                self.scalarGrid[j][i] -= ( preGrid[j-self.gridDirection[1]][i-self.gridDirection[0]] - preGrid[j][i])*Config.kConstant

    def bilinearInterpolate(self, coordinates, printStatus=False): #coordinate in real world values

        # xCoord = coordinates[0] + (self.origin[1]*Config.CellSize)
        # yCoord = coordinates[1] + (self.origin[0]*Config.CellSize)

        xCoord = coordinates[0] #- (self.origin[1]*Config.CellSize)
        yCoord = coordinates[1] #- (self.origin[0]*Config.CellSize)
        

        xCoord /= Config.CellSize
        yCoord /= Config.CellSize
        # yCoord += 1
        jIndex = int((coordinates[1])/(Config.CellSize))
        iIndex = int((coordinates[0])/(Config.CellSize))
        xPercentage = (xCoord-iIndex)
        yPercentage = (yCoord-jIndex)


        if printStatus:
            # print(coordinates)
            # print(xCoord)
            # print(yCoord)
            # print(iIndex)
            # print(jIndex)
            # print(len(self.scalarGrid[0]))
            # print()
            
            # print(xPercentage)
            # print(yPercentage)
            # print()
            pass

        # print(self.gridDirection[0])
        # print(self.scalarGrid)
        # print("\n")
        # print(coordinates)
        # print(xCoord)
        # print(yCoord)
        # print(jIndex)
        # print(iIndex)
        # print('*****')


        NWVelocity = self.scalarGrid[jIndex][iIndex]
        # print(NWVelocity)
        NEVelocity = self.scalarGrid[jIndex][iIndex+1]
        SWVelocity = self.scalarGrid[jIndex+1][iIndex]
        SEVelocity = self.scalarGrid[jIndex+1][iIndex+1]

        

        # topX = (xPercentage/Config.CellSize)*NEVelocity + ((1-xPercentage)/Config.CellSize)*NWVelocity
        # bottomX = (xPercentage/Config.CellSize)*SEVelocity + ((1-xPercentage)/Config.CellSize)*SWVelocity

        topX = (xPercentage)*NEVelocity + ((1-xPercentage))*NWVelocity
        bottomX = (xPercentage)*SEVelocity + ((1-xPercentage))*SWVelocity

        if printStatus:
            # print(NEVelocity)
            # print(NWVelocity)
            # print("topx",topX)
            # print("botomx",bottomX)
            # print("ypercentage",yPercentage)
            pass

        # interpolatedScalar = (yPercentage/Config.CellSize)*bottomX + ((1-yPercentage)/Config.CellSize)*topX
        interpolatedScalar = (yPercentage)*bottomX + ((1-yPercentage))*topX

        if interpolatedScalar != 0 and printStatus==True:
            print(xPercentage)
            print(yPercentage)
            print()
        # print(interpolatedScalar)
        # print('\n')
        return interpolatedScalar
    
    def advectVelocities(self, hVectorField, vVectorField):
        for j in range(2,self.rows-2):
            for i in range(2,self.columns-2):
                # coordinates = [(i+hVectorField.origin[0])*Config.CellSize,(j+hVectorField.origin[1])*Config.CellSize]
                # coordinates = ((i+self.origin[0])*Config.CellSize,(j+self.origin[1])*Config.CellSize)

                #first line creates waves
                # coordinates = ((i+self.origin[0])*Config.CellSize, (j+self.origin[1])*Config.CellSize)
                coordinates = ((i+self.origin[1])*Config.CellSize, (j+self.origin[0])*Config.CellSize)

                #the coordinates should take into account the vector field's origin
                # coordinates = ((i)*Config.CellSize,(j)*Config.CellSize)

                hVelocity = hVectorField.bilinearInterpolate(coordinates, False)

                # hVelocity = hVectorField.scalarGrid[j][i]

                hdistance = hVelocity*((-1)*Config.timeStep)
                # coordinates = [(i+vVectorField.origin[0])*Config.CellSize,(j+vVectorField.origin[1])*Config.CellSize]
                vVelocity = vVectorField.bilinearInterpolate(coordinates, False)
                # vVelocity = vVectorField.scalarGrid[j][i]
                vdistance = vVelocity*((-1)*Config.timeStep)

                # xCoord = i*Config.CellSize - (self.gridDirection[0]*hdistance)
                # yCoord = j*Config.CellSize - (self.gridDirection[1]*vdistance)


                # print("Hvelocity:",hVelocity)
                # print(hdistance)

                xCoord = (i*Config.CellSize) + hdistance
                yCoord = (j*Config.CellSize) + vdistance

                # print("\n")
                # print('xcoord: ' ,xCoord)
                # print("ycoord",yCoord)
                # print("***")
                
                if self.gridDirection[0] == 1:
                    # print("horizontal error")
                    self.scalarGrid[j][i] = hVectorField.bilinearInterpolate((xCoord,yCoord), False)
                    # print("horizontal",self.scalarGrid[j][i])

                elif self.gridDirection[1] == 1:
                    # print("vertical error")
                    self.scalarGrid[j][i] = vVectorField.bilinearInterpolate((xCoord,yCoord), False)
                    # print("vertical",self.scalarGrid[j][i])
                

    
class VisualVectorField(VectorField):
    def __init__(self, rows, columns, colour, origin, gridDirection):
        super().__init__(rows, columns, colour, origin, gridDirection)
        self.vectorGrid = []

        for x in range(rows): #arranged as a list containing lists of all values in a row
            self.vectorGrid.append([])
            for _ in range(columns):
                self.vectorGrid[x].append([0,0])
    
    def interpolateUpscaledGrid(self, hVectorField, vVectorField):
        for j in range(Config.upscaleConstant, self.rows-Config.upscaleConstant): 
            for i in range(Config.upscaleConstant, self.columns-Config.upscaleConstant):

                #calculate real world coordinates of each grid point
                yCoord = j*Config.CellSize/Config.upscaleConstant
                xCoord = i*Config.CellSize/Config.upscaleConstant

                # yCoord += self.origin[0]*Config.CellSize
                # xCoord += self.origin[1]*Config.CellSize
                # print(xCoord)
                # print(yCoord)

                #use real world coordinates to calculate vector value
                self.vectorGrid[j][i] = [hVectorField.bilinearInterpolate([xCoord,yCoord], False), 
                                         vVectorField.bilinearInterpolate([xCoord,yCoord], False)]
                
               
    def drawVectorField(self, screen):
        xOffset = Config.GridOrigin[0] + (self.origin[0]*Config.CellVisualSize)
        yOffset = Config.GridOrigin[1] + (self.origin[1]*Config.CellVisualSize)
        cellSize = Config.VisualVectorCellSize

        # cellCenter = cellSize/2
        for jIndex, rowList in enumerate(self.vectorGrid):
            for iIndex, vector in enumerate(rowList):
                vectorStart = (xOffset+cellSize*iIndex, yOffset+cellSize*jIndex)
                vector = [self.gridDirection[0]*vector[0], self.gridDirection[1]*vector[1]]
                vectorEndX = xOffset+cellSize*iIndex+vector[0]*Config.VectorVisualScale
                vectorEndY = yOffset+cellSize*jIndex+vector[1]*Config.VectorVisualScale

                self.drawVector(screen, vectorStart, (vectorEndX,vectorEndY), drawTail=True)
                
                # pygame.draw.line(screen, self.colour, vectorStart, (vectorEndX, vectorEndY))
                # pygame.draw.circle(screen,self.colour, (vectorEndX, vectorEndY), Config.VectorBallRadius)




                

class DivergenceField(ScalarGrid):
    def __init__(self, rows, columns, origin):
        super().__init__(rows, columns, origin)
    
    def calculateDivergence(self, HVectors, VVectors):
        HVectors = HVectors.scalarGrid
        VVectors = VVectors.scalarGrid
        for j in range(self.rows):
            for i in range(self.columns):
                self.scalarGrid[j][i] = ((HVectors[j][i] - HVectors[j][i+1]) + (VVectors[j][i] - VVectors[j+1][i])) #/Config.CellSize #this bastard ruined my life


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
                        self.scalarGrid[0][i] = np.float64(1)
            case "east":
                for j in range(self.rows):
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
        match wallDirection:
            case "north":
                for i in range(self.columns):
                        self.scalarGrid[0][i] = np.float64(3)
            case "east":
                for j in range(self.rows):
                        self.scalarGrid[j][self.columns-1] = np.float64(3)
            case "south":
                for i in range(self.columns):
                # for j in range(self.rows):
                #     for i in range(self.columns):
                        self.scalarGrid[self.rows-1][i] = np.float64(3)
            case "west":
                for j in range(self.rows):
                # for j in range(self.rows):
                #     for i in range(self.columns):
                        self.scalarGrid[j][0] = np.float64(3)



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

    # def GaussSeidelLoopDebug(self, divGrid, cellMap):
    #     for _ in range (Config.GaussSeidelIterations):
    #         x = input("?")
    #         self.calculatePressureGrid(divGrid, cellMap)

    def calculatePressureGrid(self, divGrid, cellMap):
        divGrid = divGrid.scalarGrid
        for j in range(1,self.rows-1):
            for i in range(1,self.columns-1):
                right = self.findNeighbourPressureValue(j, i, [0,1], cellMap)
                left = self.findNeighbourPressureValue(j,i,[0,-1], cellMap)
                top = self.findNeighbourPressureValue(j,i,[-1,0], cellMap)
                bottom = self.findNeighbourPressureValue(j,i,[1,0], cellMap)

                self.scalarGrid[j][i] = (right + left + top + bottom - ( (divGrid[j][i])/Config.kConstant ) )/4

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



