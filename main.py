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

temphVectorField = ScalarGridChildren.VectorField(Config.rowCount, Config.columnCount+1, Config.WHITE, (0, 0.5), (1,0)) 
tempvVectorField = ScalarGridChildren.VectorField(Config.rowCount+1, Config.columnCount, Config.LIGHTGREY, (0.5, 0), (0,1)) 


cellMapGrid.setWallVoid('north')
cellMapGrid.setWallVoid('east')
cellMapGrid.setWallVoid('south')
cellMapGrid.setWallVoid('west')
hVectorField.setBoundaryConditions(cellMapGrid)
vVectorField.setBoundaryConditions(cellMapGrid)



running = True
while running:
    
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print('new iteration')
                
                temphVectorField.advectVelocities(hVectorField, vVectorField)
                tempvVectorField.advectVelocities(hVectorField, vVectorField)

                hVectorField.scalarGrid = list(temphVectorField.scalarGrid)
                vVectorField.scalarGrid = list(tempvVectorField.scalarGrid)

                divergenceGrid.calculateDivergence(hVectorField,vVectorField)
                
                pressureGrid.GaussSeidelLoop(divergenceGrid,cellMapGrid)

                hVectorField.calculateVelocityGrid(pressureGrid)
                vVectorField.calculateVelocityGrid(pressureGrid)

                hVectorField.setBoundaryConditions(cellMapGrid)
                vVectorField.setBoundaryConditions(cellMapGrid)


            if event.key == pygame.K_0:
                hVectorField.setZero()
                vVectorField.setZero()
            if event.key == pygame.K_r:
                hVectorField.scalarGrid[7][7] -= 0.0025
            if event.key == pygame.K_t:
                hVectorField.scalarGrid[7][7] += 0.000025
            if event.key == pygame.K_f:
                vVectorField.scalarGrid[3][4] -= 0.000025
            if event.key == pygame.K_g:
                # vVectorField.scalarGrid[7][7] += 0.000025
                vVectorField.scalarGrid[3][7] += 3


    if True:
        temphVectorField.advectVelocities(hVectorField, vVectorField)
        tempvVectorField.advectVelocities(hVectorField, vVectorField)

        hVectorField.scalarGrid = list(temphVectorField.scalarGrid)
        vVectorField.scalarGrid = list(tempvVectorField.scalarGrid)

        # for x in range(7,20):
        #     vVectorField.scalarGrid[7][7] = 3

        # divergenceGrid.calculateDivergence(hVectorField,vVectorField)
        
        # pressureGrid.GaussSeidelLoop(divergenceGrid,cellMapGrid)

        # hVectorField.calculateVelocityGrid(pressureGrid)
        # vVectorField.calculateVelocityGrid(pressureGrid)

        # hVectorField.setBoundaryConditions(cellMapGrid)
        # vVectorField.setBoundaryConditions(cellMapGrid)


    # hVectorField.drawVectorField(screen)
    # vVectorField.drawVectorField(screen)
    # pressureGrid.drawGrid(screen)
    # vVectorField.scalarGrid[3][3] += 3


    visualVectorField.interpolateUpscaledGrid(hVectorField,vVectorField)
    visualVectorField.drawVectorField(screen)

    # temphVectorField.drawVectorField(screen)
    # tempvVectorField.drawVectorField(screen)
    # divergence on bottom
    # pressureGrid.labelScalars(screen, textFont)
    # divergenceGrid.labelScalars(screen, textFont)





    pygame.display.flip()
    screen.fill(Config.BLACK)

    # Cap the frame rate
    clock.tick()

# Quit Pygame
pygame.quit()
