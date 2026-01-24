SCREENWIDTH = 1900
SCREENHEIGHT = 1200

rowCount = 30
columnCount = 50 #in context of centered grids
GaussSeidelIterations = 30


GridOrigin = [15,15]
fluidDensity = 1.225 #kg/m^3
# fluidDensity = 1.9
CellSize = 0.5 # meters
timeStep = 0.1 # seconds
kConstant = timeStep/(CellSize*fluidDensity)
# kConstant = 1

manualVelocityInjection = 0.5


CellVisualSize = 35
ScalarFontSize = 20
ScalarGridRoundingCutoff = 1

# VectorVisualScale = 10**6
VectorVisualScale = 30
VectorBallRadius = 1

upscaleConstant = 3

VisualVectorCellSize = CellVisualSize/upscaleConstant



BLACK = [0,0,0]
WHITE = [255,255,255]
LIGHTGREY = [200,200,200]
RED = [255,0,0]
GREEN = [0,255,0]
BLUE = [0,0,255]