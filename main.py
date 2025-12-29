import pygame
import Config
import ScalarGridChildren 

pygame.init()

screen = pygame.display.set_mode((Config.SCREENWIDTH, Config.SCREENHEIGHT))
pygame.display.set_caption("2D CFD")

clock = pygame.time.Clock()

pressureGrid = ScalarGridChildren.PressureField(Config.rowCount,Config.columnCount, (0,0))
divergenceGrid = ScalarGridChildren.DivergenceField(Config.rowCount, Config.columnCount, (0,0.2))
cellMapGrid = ScalarGridChildren.CellMap(Config.rowCount, Config.columnCount, (0,0))

#3 rows of centered grid cells is equal to 4 rows of vectors |#|#|#|
hVectorField = ScalarGridChildren.VectorField(Config.rowCount, Config.columnCount+1, Config.RED, (0, 0.5), (1,0)) 
vVectorField = ScalarGridChildren.VectorField(Config.rowCount+1, Config.columnCount, Config.GREEN, (0.5, 0), (0,1))


textFont = pygame.font.Font(None, Config.ScalarFontSize)

# hVectorField.randomizeScalarField()
# vVectorField.randomizeScalarField()
divergenceGrid.calculateDivergence(hVectorField,vVectorField)
pressureGrid.calculatePressureGrid(divergenceGrid, cellMapGrid)

# temphVectorField = ScalarGridChildren.VectorField(Config.rowCount, Config.columnCount+1, (0.5, 0)) 
# tempvVectorField = ScalarGridChildren.VectorField(Config.rowCount+1, Config.columnCount, (0, 0.5))
visualVectorField = ScalarGridChildren.VisualVectorField(Config.rowCount*Config.upscaleConstant,
                                                         Config.columnCount*Config.upscaleConstant,
                                                         Config.BLUE, (0.5,0.5), (1,1))

temphVectorField = ScalarGridChildren.VectorField(Config.rowCount, Config.columnCount+1, Config.RED, (0, 0.5), (1,0)) 
tempvVectorField = ScalarGridChildren.VectorField(Config.rowCount+1, Config.columnCount, Config.GREEN, (0.5, 0), (0,1)) 


cellMapGrid.setWallSolid('north')
cellMapGrid.setWallSolid('east')
cellMapGrid.setWallSolid('south')
cellMapGrid.setWallSolid('west')
hVectorField.setBoundaryConditions(cellMapGrid)
vVectorField.setBoundaryConditions(cellMapGrid)



running = True
while running:
    
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # temphVectorField.advectVelocities(hVectorField, vVectorField)
                # tempvVectorField.advectVelocities(vVectorField, vVectorField)
                # hVectorField.scalarGrid = temphVectorField.scalarGrid
                # vVectorField.scalarGrid = tempvVectorField.scalarGrid

                divergenceGrid.calculateDivergence(hVectorField,vVectorField)
                

                pressureGrid.GaussSeidelLoop(divergenceGrid,cellMapGrid)
                # pressureGrid.GaussSeidelLoopDebug(divergenceGrid,cellMapGrid, screen, textFont)

                hVectorField.calculateVelocityGrid(pressureGrid)
                vVectorField.calculateVelocityGrid(pressureGrid)

                hVectorField.setBoundaryConditions(cellMapGrid)
                vVectorField.setBoundaryConditions(cellMapGrid)


            if event.key == pygame.K_0:
                hVectorField.setZero()
                vVectorField.setZero()
            if event.key == pygame.K_r:
                hVectorField.scalarGrid[3][4] -= 0.25
            if event.key == pygame.K_t:
                hVectorField.scalarGrid[3][4] += 0.25
            if event.key == pygame.K_f:
                vVectorField.scalarGrid[3][4] -= 0.25
            if event.key == pygame.K_g:
                vVectorField.scalarGrid[3][4] += 0.25


    divergenceGrid.calculateDivergence(hVectorField,vVectorField)
    # pressureGrid.GaussSeidelLoop(divergenceGrid, cellMapGrid)

    # pressureGrid.calculatePressureGrid(divergenceGrid,cellMapGrid)

    # hVectorField.calculateVelocityGrid(pressureGrid)
    # vVectorField.calculateVelocityGrid(pressureGrid)

    # hVectorField.setBoundaryConditions(cellMapGrid)
    # vVectorField.setBoundaryConditions(cellMapGrid)

    # temphVectorField.advectVelocities(hVectorField)
    # tempvVectorField.advectVelocities(vVectorField)
    # hVectorField.scalarGrid = temphVectorField.scalarGrid
    # vVectorField.scalarGrid = tempvVectorField.scalarGrid

    # divergenceGrid.calculateDivergence(hVectorField,vVectorField)
    # print(hVectorField.scalarGrid)
    visualVectorField.interpolateUpscaledGrid(hVectorField,vVectorField)

    visualVectorField.drawVectorField(screen)

    # hVectorField.drawVectorField(screen)
    # vVectorField.drawVectorField(screen)
    # pressureGrid.drawGrid(screen)
    # # divergence on bottom
    # pressureGrid.labelScalars(screen, textFont)
    # divergenceGrid.labelScalars(screen, textFont)





    pygame.display.flip()
    screen.fill(Config.BLACK)

    # Cap the frame rate
    clock.tick()

# Quit Pygame
pygame.quit()
