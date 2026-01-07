SCREENWIDTH = 1000
SCREENHEIGHT = 700

rowCount = 25
columnCount = 30 #in context of centered grids
GaussSeidelIterations = 50


GridOrigin = [15,15]
fluidDensity = 1.225 #kg/m^3
CellSize = 0.0001 # meters
timeStep = 0.0001 # seconds
kConstant = timeStep/(CellSize*fluidDensity)
# kConstant = 1


CellVisualSize = 25
ScalarFontSize = 20
ScalarGridRoundingCutoff = 1

# VectorVisualScale = 10**6
VectorVisualScale = 30
VectorBallRadius = 3

upscaleConstant = 3

VisualVectorCellSize = CellVisualSize/upscaleConstant



BLACK = [0,0,0]
WHITE = [255,255,255]
LIGHTGREY = [200,200,200]
RED = [255,0,0]
GREEN = [0,255,0]
BLUE = [0,0,255]