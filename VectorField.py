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
                self.HVectors[x].append(np.float64(0))
                
        for y in range(rows+1): #Vvectors arranged as a list of lists containing all vectors in a row
            self.VVectors.append([])
            for _ in range(columns):
                self.VVectors[y].append(np.float64(0))  


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
                vectorEndX = xOffset+cellSize*iIndex+vector*Config.VectorVisualScale
                vectorEndY = yOffset+cellCenter+cellSize*jIndex

                pygame.draw.line(screen, Config.RED, vectorStart, (vectorEndX, vectorEndY))
                pygame.draw.circle(screen,Config.RED, (vectorEndX, vectorEndY), Config.VectorBallRadius)

        for jIndex, rowList in enumerate(self.VVectors):
            for iIndex, vector in enumerate(rowList):
                vectorStart = (xOffset+cellCenter+cellSize*iIndex, yOffset+cellSize*jIndex)
                vectorEndX = xOffset+cellCenter+cellSize*iIndex
                vectorEndY = yOffset+cellSize*jIndex+vector*Config.VectorVisualScale

                pygame.draw.line(screen, Config.GREEN, vectorStart,(vectorEndX, vectorEndY))
                pygame.draw.circle(screen,Config.GREEN, (vectorEndX, vectorEndY), Config.VectorBallRadius)


    def randomizeVectorField(self):
        for jIndex in range(self.HVrows):
            for iIndex in range(self.HVcolumns):
                self.HVectors[jIndex][iIndex] = np.float64(random.random()*5-2.5)
        for jIndex in range(self.VVrows):
            for iIndex in range(self.VVcolumns):
                self.VVectors[jIndex][iIndex] = np.float64(random.random()*5-2.5)

    def drawVector(self, screen, vector, color):
        # pygame.draw.line(screen, )
        pass
        