import pygame
import Config
import ScalarGridChildren 
import math

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
                                                         Config.BLUE, (0,0), (1,1))

temphVectorField = ScalarGridChildren.VectorField(Config.rowCount, Config.columnCount+1, Config.WHITE, (0, 0.5), (1,0)) 
tempvVectorField = ScalarGridChildren.VectorField(Config.rowCount+1, Config.columnCount, Config.LIGHTGREY, (0.5, 0), (0,1)) 


cellMapGrid.setWallVoid('north')
cellMapGrid.setWallVoid('east')
cellMapGrid.setWallVoid('south')
cellMapGrid.setWallVoid('west')
hVectorField.setBoundaryConditions(cellMapGrid)
vVectorField.setBoundaryConditions(cellMapGrid)

circleX = -5
circleY = 2
# for x in range(5):
#     for y in range(5):
#         cellMapGrid.scalarGrid[10+y][10+x] = 1

cellMapGrid.scalarGrid[13+circleY][15+circleX] = 1
cellMapGrid.scalarGrid[14+circleY][15+circleX] = 1
cellMapGrid.scalarGrid[15+circleY][15+circleX] = 1
cellMapGrid.scalarGrid[16+circleY][15+circleX] = 1
cellMapGrid.scalarGrid[17+circleY][15+circleX] = 1

cellMapGrid.scalarGrid[14+circleY][14+circleX] = 1
cellMapGrid.scalarGrid[15+circleY][14+circleX] = 1
cellMapGrid.scalarGrid[16+circleY][14+circleX] = 1

cellMapGrid.scalarGrid[15+circleY][13+circleX] = 1

cellMapGrid.scalarGrid[14+circleY][16+circleX] = 1
cellMapGrid.scalarGrid[15+circleY][16+circleX] = 1
cellMapGrid.scalarGrid[16+circleY][16+circleX] = 1

cellMapGrid.scalarGrid[15+circleY][17+circleX] = 1

realWorldTime = 0




velocityViewStatus = False
viewPressureStatus = False

runStatus = False
running = True
while running:
    realWorldTime += Config.timeStep
    print(realWorldTime)
    

    mouseCoords = [0,0]
    mouseCoords[0] = pygame.mouse.get_pos()[0]
    mouseCoords[1] = pygame.mouse.get_pos()[1]
    mouseCoords[0] -= Config.GridOrigin[0]
    mouseCoords[1] -= Config.GridOrigin[1]

    mouseCoords[0] /= Config.CellVisualSize
    mouseCoords[1] /= Config.CellVisualSize

    mouseCoords[0] = int(mouseCoords[0])
    mouseCoords[1] = int(mouseCoords[1])
    if pygame.mouse.get_pressed()[0]:
        cellMapGrid.scalarGrid[mouseCoords[1]][mouseCoords[0]] = 1
    if pygame.mouse.get_pressed()[2]:
        cellMapGrid.scalarGrid[mouseCoords[1]][mouseCoords[0]] = 0

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

                # divergenceGrid.calculateDivergence(hVectorField,vVectorField)
                
                # pressureGrid.GaussSeidelLoop(divergenceGrid,cellMapGrid)

                # hVectorField.calculateVelocityGrid(pressureGrid)
                # vVectorField.calculateVelocityGrid(pressureGrid)

                # hVectorField.setBoundaryConditions(cellMapGrid)
                # vVectorField.setBoundaryConditions(cellMapGrid)


            if event.key == pygame.K_0:
                hVectorField.setZero()
                vVectorField.setZero()
            if event.key == pygame.K_r:
                hVectorField.scalarGrid[20][5] -= Config.manualVelocityInjection
            if event.key == pygame.K_t:
                hVectorField.scalarGrid[20][5] += Config.manualVelocityInjection
            if event.key == pygame.K_f:
                vVectorField.scalarGrid[20][5] -= Config.manualVelocityInjection
            if event.key == pygame.K_g:
                # vVectorField.scalarGrid[7][7] += 0.000025
                vVectorField.scalarGrid[20][5] += Config.manualVelocityInjection
            if event.key == pygame.K_v:
                velocityViewStatus = not velocityViewStatus
            
            if event.key == pygame.K_w:
                runStatus = not runStatus
            if event.key == pygame.K_p:
                viewPressureStatus = not viewPressureStatus


            # if pygame.key.get_pressed()[pygame.K_b]:
            #     print
            #     cellMapGrid.scalarGrid[12][20] = 1
            #     print("SOLDICUBE")
            # else:
            #     cellMapGrid.scalarGrid[12][20] = 0

    # print("horizontal")
    # print(hVectorField.bilinearInterpolate([25*Config.CellSize, 20*Config.CellSize], printStatus=False))
    # print("vertical")
    # print(vVectorField.bilinearInterpolate([25*Config.CellSize, 20*Config.CellSize], printStatus=False))

    if runStatus:
        # vVectorField.scalarGrid[20][25] = Config.manualVelocityInjection
        # hVectorField.scalarGrid[12][5] = Config.manualVelocityInjection

        for row in range(Config.rowCount):
            hVectorField.scalarGrid[row][3] = Config.manualVelocityInjection

        

        # pressureGrid.scalarGrid[15][10] = -500
        
        # vVectorField.scalarGrid[50][35] = -Config.manualVelocityInjection

        if True:
            temphVectorField.advectVelocities(hVectorField, vVectorField)
            tempvVectorField.advectVelocities(hVectorField, vVectorField)

            hVectorField.scalarGrid = list(temphVectorField.scalarGrid)
            vVectorField.scalarGrid = list(tempvVectorField.scalarGrid)
            
            pass
        if True:
            divergenceGrid.calculateDivergence(hVectorField,vVectorField)
            
            pressureGrid.GaussSeidelLoop(divergenceGrid,cellMapGrid)

            hVectorField.calculateVelocityGrid(pressureGrid)
            vVectorField.calculateVelocityGrid(pressureGrid)

            hVectorField.setBoundaryConditions(cellMapGrid)
            vVectorField.setBoundaryConditions(cellMapGrid)
            pass
        pass




    
    
    # pressureGrid.drawGrid(screen)

    
    if not velocityViewStatus:
        visualVectorField.interpolateUpscaledGrid(hVectorField,vVectorField)
        visualVectorField.drawVectorField(screen)

    if velocityViewStatus:
        for y in range(Config.rowCount-1):
            for x in range(Config.columnCount-1):
                coord = [(0.5+x)*Config.CellSize, (0.5+y)*Config.CellSize]
                xVelocity = hVectorField.bilinearInterpolate(coord)
                yVelocity = vVectorField.bilinearInterpolate(coord)
                trueVelocity = math.sqrt(xVelocity*xVelocity + yVelocity*yVelocity)

                rect = (Config.GridOrigin[0]+x*Config.CellVisualSize, Config.GridOrigin[1]+y*Config.CellVisualSize, Config.CellVisualSize, Config.CellVisualSize)

                maxVelocity = 0.75

                percentage = trueVelocity/maxVelocity*255
                if percentage > 255:
                    percentage = 255

                colour = [255-percentage,percentage,0]
                pygame.draw.rect(screen, colour, rect)

    cellMapGrid.drawCellMap(screen)

    hVectorField.drawVectorField(screen)
    vVectorField.drawVectorField(screen)

    # print(hVectorField.bilinearInterpolate([25*Config.CellSize,20*Config.CellSize], printStatus=False) )
    # print(vVectorField.bilinearInterpolate([25*Config.CellSize,20*Config.CellSize]) )
    # print()


    # temphVectorField.drawVectorField(screen)
    # tempvVectorField.drawVectorField(screen)
    # divergence on bottom
    if viewPressureStatus:
        pressureGrid.labelScalars(screen, textFont)
    # divergenceGrid.labelScalars(screen, textFont)





    pygame.display.flip()
    screen.fill(Config.BLACK)

    # Cap the frame rate
    clock.tick()

# Quit Pygame
pygame.quit()
