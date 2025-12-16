import numpy as np
import pygame
import Config
import random

class VectorField:
    def __init__(self, rows, columns): #rows and columns come in terms of centered grid cells
        #3 rows of centered grid cells is equal to 4 rows of vectors |#|#|#|

        self.HVrows = rows
        self.HVcolumns = columns+1

        self.VVrows = rows+1
        self.VVcolumns = columns

        self.HVectors = []
        self.VVectors = []
        #  _ _ _ _ _
        # |#|#|#|#|#|
        #  - - - - -
        # |#|#|#|#|#|
        #  _ _ _ _ _

        for x in range(rows): #Hvectors arranged as a list of lists containing all vectors in a row
            self.HVectors.append([])
            for _ in range(columns+1):
                self.HVectors[x].append(np.array([np.float64(0),np.float64(0)]))
        print(len(self.HVectors))
        print(len(self.HVectors[0]))
                
        for y in range(rows+1): #Vvectors arranged as a list of lists containing all vectors in a row
            self.VVectors.append([])
            for _ in range(columns):
                self.VVectors[y].append(np.array([np.float64(0),np.float64(0)]))  


        # for _ in range(rows+1):
        #     self.HVectors.append(np.float64(0))
        # for _ in range(columns+1):
        #     self.VVectors.append(np.float64(0))
        

    def drawVectorField(self, screen):
        xOffset = Config.GridOrigin[0]
        yOffset = Config.GridOrigin[1]
        cellSize = Config.CellVisualSize
        cellCenter = cellSize/2
        for jIndex, rowList in enumerate(self.HVectors):
            for iIndex, vector in enumerate(rowList):
                vectorStart = (xOffset+cellSize*iIndex, yOffset+cellCenter+cellSize*jIndex)
                vectorEndX = xOffset+cellSize*iIndex+vector[0]*Config.VectorVisualScale
                vectorEndY = yOffset+cellCenter+cellSize*jIndex+vector[1]*Config.VectorVisualScale

                pygame.draw.line(screen, Config.RED, vectorStart, (vectorEndX, vectorEndY))
                pygame.draw.circle(screen,Config.RED, (vectorEndX, vectorEndY), 5)
        
        for jIndex, rowList in enumerate(self.VVectors):
            for iIndex, vector in enumerate(rowList):
                vectorStart = (xOffset+cellCenter+cellSize*iIndex, yOffset+cellSize*jIndex)
                vectorEndX = xOffset+cellCenter+cellSize*iIndex+vector[0]*Config.VectorVisualScale
                vectorEndY = yOffset+cellSize*jIndex+vector[1]*Config.VectorVisualScale

                pygame.draw.line(screen, Config.GREEN, vectorStart,(vectorEndX, vectorEndY))
                pygame.draw.circle(screen,Config.GREEN, (vectorEndX, vectorEndY), 5)


    def randomizeVectorField(self):
        for jIndex in range(self.HVrows):
            for iIndex in range(self.HVcolumns):
                self.HVectors[jIndex][iIndex] = np.array([random.random()*10,random.random()*10])


    def drawVector(self, screen, vector, color):
        # pygame.draw.line(screen, )
        pass
        