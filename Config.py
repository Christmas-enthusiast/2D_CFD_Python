SCREENWIDTH = 900
SCREENHEIGHT = 600

rowCount = 6
columnCount = 8 #in context of centered grids
GaussSeidelIterations = 30


GridOrigin = [15,15]
fluidDensity = 1.225 #kg/m^3
CellSize = 0.1 # meters
timeStep = 0.1 # seconds
# kConstant = timeStep/(CellSize*fluidDensity)
kConstant = 1


CellVisualSize = 90
ScalarFontSize = 20
ScalarGridRoundingCutoff = 3

VectorVisualScale = 1
VectorBallRadius = 2

upscaleConstant = 4

VisualVectorCellSize = CellVisualSize/upscaleConstant



BLACK = [0,0,0]
WHITE = [255,255,255]
RED = [255,0,0]
GREEN = [0,255,0]
BLUE = [0,0,255]