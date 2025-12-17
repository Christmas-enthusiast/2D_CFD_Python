import pygame
import Config
import ScalarGridChildren 

pygame.init()

screen = pygame.display.set_mode((Config.SCREENWIDTH, Config.SCREENHEIGHT))
pygame.display.set_caption("2D CFD")

clock = pygame.time.Clock()

pressureGrid = ScalarGridChildren.PressureField(Config.rowCount,Config.columnCount)
divergenceGrid = ScalarGridChildren.DivergenceField(Config.rowCount, Config.columnCount)
cellMapGrid = ScalarGridChildren.CellMap(Config.rowCount, Config.columnCount)

#3 rows of centered grid cells is equal to 4 rows of vectors |#|#|#|
hVectorField = ScalarGridChildren.VectorField(Config.rowCount, Config.columnCount+1) 
vVectorField = ScalarGridChildren.VectorField(Config.rowCount+1, Config.columnCount)


textFont = pygame.font.Font(None, Config.ScalarFontSize)

hVectorField.randomizeScalarField()
vVectorField.randomizeScalarField()
divergenceGrid.calculateDivergence(hVectorField,vVectorField)
pressureGrid.calculatePressureGrid(divergenceGrid, cellMapGrid)

cellMapGrid.setWallSolid('north')
cellMapGrid.setWallSolid('east')
cellMapGrid.setWallSolid('south')
cellMapGrid.setWallSolid('west')
hVectorField.setHorizontalBoundaryConditions(cellMapGrid)
vVectorField.setVerticalBoundaryConditions(cellMapGrid)


running = True
while running:
    
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                divergenceGrid.calculateDivergence(hVectorField,vVectorField)

                pressureGrid.GaussSeidelLoop(divergenceGrid,cellMapGrid)
         

                hVectorField.calculateHorizontalVelocityGrid(pressureGrid)
                vVectorField.calculateVerticalVelocityGrid(pressureGrid)

                hVectorField.setHorizontalBoundaryConditions(cellMapGrid)
                vVectorField.setVerticalBoundaryConditions(cellMapGrid)
                print('test')
            if event.key == pygame.K_r:
                hVectorField.scalarGrid[3][4] += 1

    divergenceGrid.calculateDivergence(hVectorField,vVectorField)
    hVectorField.drawHorizontalVectorField(screen)
    vVectorField.drawVerticalVectorField(screen)
    

                
    # pressureGrid.calculatePressureGrid(divergenceGrid, cellMapGrid)

    divergenceGrid.labelScalars(screen, textFont)





    pygame.display.flip()
    screen.fill(Config.BLACK)

    # Cap the frame rate
    clock.tick()

# Quit Pygame
pygame.quit()
