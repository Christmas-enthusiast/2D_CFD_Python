import numpy as np
import pygame

class CenteredGrid:
    def __init__(self, rows, columns):

        # self.HScalars = []
        # self.VScalars = []

        self.scalarGrid = []
        
        for x in range(rows):
            self.scalarGrid.append([])
            for _ in range(columns):
                self.scalarGrid[x].append(np.float64(0))

        # for x in range(columns):
        #     self.HScalars.append([])
        #     for _ in range(rows):
        #         self.HScalars[x].append(np.float64(0))
                
        # for y in range(rows):
        #     self.VScalars.append([])
        #     for _ in range(columns):
        #         self.VScalars[y].append(np.float64(0))   
                

        # for _ in range(rows):
        #     self.HScalars.append(np.float64(0))
        # for _ in range(columns):
        #     self.VScalars.append(np.float64(0))
    
    def labelScalars(self, screen):
        pass