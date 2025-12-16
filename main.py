import pygame
import Config
from CenteredGrid import ScalarGrid

pygame.init()

screen = pygame.display.set_mode((Config.SCREENWIDTH, Config.SCREENHEIGHT))
pygame.display.set_caption("2D CFD")

clock = pygame.time.Clock()

testGrid = ScalarGrid(Config.rowCount,Config.columnCount)
#3 rows of centered grid cells is equal to 4 rows of vectors |#|#|#|
hVectorField = ScalarGrid(Config.rowCount, Config.columnCount+1) 
vVectorField = ScalarGrid(Config.rowCount+1, Config.columnCount)
textFont = pygame.font.Font(None, 30)

hVectorField.randomizeScalarField()
vVectorField.randomizeScalarField()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    testGrid.labelScalars(screen, textFont)
    hVectorField.drawHorizontalVectorField(screen)
    vVectorField.drawVerticalVectorField(screen)




    pygame.display.flip()
    screen.fill(Config.BLACK)

    # Cap the frame rate
    clock.tick()

# Quit Pygame
pygame.quit()
