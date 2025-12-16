import pygame
import Config
from CenteredGrid import CenteredGrid
from VectorField import VectorField

pygame.init()

screen = pygame.display.set_mode((Config.SCREENWIDTH, Config.SCREENHEIGHT))
pygame.display.set_caption("2D CFD")

clock = pygame.time.Clock()

testGrid = CenteredGrid(2,5)
vectorField = VectorField(2,5)
textFont = pygame.font.Font(None, 30)

vectorField.randomizeVectorField()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    testGrid.labelScalars(screen, textFont)
    vectorField.drawVectorField(screen)




    pygame.display.flip()
    screen.fill(Config.BLACK)

    # Cap the frame rate
    clock.tick()

# Quit Pygame
pygame.quit()
