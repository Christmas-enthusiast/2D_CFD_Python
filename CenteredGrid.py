import numpy as np
import pygame
import Config
import random

class ScalarGrid:
    def __init__(self, rows, columns):

        # self.HScalars = []
        # self.VScalars = []
        self.rows = rows
        self.columns = columns

        self.scalarGrid = []
        
        for x in range(rows): #arranged as a list containing lists of all values in a row
            self.scalarGrid.append([])
            for _ in range(columns):
                self.scalarGrid[x].append(np.float64(0))



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


    def drawGrid(self, screen):
        xOffset = Config.GridOrigin[0]
        yOffset = Config.GridOrigin[1]
        cellSize = Config.CellVisualSize
        for rows in range(self.rows+1):
            pygame.draw.line(screen, Config.WHITE, #horizontal lines
                             (xOffset, yOffset+(rows+0)*cellSize), 
                             (xOffset+cellSize*self.columns, yOffset+(rows+0)*cellSize))
            
        for columns in range(self.columns+1): #vertical lines
            pygame.draw.line(screen, Config.WHITE, 
                             (xOffset+cellSize*(columns-0), yOffset),
                             (xOffset+cellSize*(columns-0),yOffset+cellSize*self.rows))
    

    def labelScalars(self, screen, font):
        self.drawGrid(screen)
        cellCenter = Config.CellVisualSize/2

        for jIndex, rowList in enumerate((self.scalarGrid)):
            for iIndex, scalarValue in enumerate(rowList):
                test = font.render(str(scalarValue),10,Config.WHITE)
                screen.blit(test, (Config.GridOrigin[0]+(cellCenter*0)+Config.CellVisualSize*iIndex, 
                                   Config.GridOrigin[1]+(cellCenter*0)+Config.CellVisualSize*jIndex))


    def randomizeScalarField(self):
        for jIndex in range(self.rows):
            for iIndex in range(self.columns):
                self.scalarGrid[jIndex][iIndex] = np.float64(random.random()*5-2.5)

    def calculateDivergence(self, VectorField):
        for jIndex in range(self.rows):
            for iIndex in range(self.columns):
                pass