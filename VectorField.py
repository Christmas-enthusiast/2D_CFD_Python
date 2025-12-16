import numpy as np


class VectorField:
    def __init__(self, rows, columns): #rows and columns come in terms of pressure cells
        #3 rows of pressure cells is equal to 4 rows of vectors |#|#|#|

        self.HVectors = []
        self.VVectors = []

        # |#|#|#|#|#|
        # |#|#|#|#|#|
        for x in range(columns+1):
            self.HVectors.append([])
            for _ in range(rows+1):
                self.HVectors[x].append(np.float64(0))
                
        for y in range(rows+1):
            self.VVectors.append([])
            for _ in range(columns+1):
                self.VVectors[y].append(np.float64(0))  


        # for _ in range(rows+1):
        #     self.HVectors.append(np.float64(0))
        # for _ in range(columns+1):
        #     self.VVectors.append(np.float64(0))
        

        