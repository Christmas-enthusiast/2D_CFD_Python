import pygame
import Config
# from CenteredGrid import CenteredGrid

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D CFD")

clock = pygame.time.Clock()

# testGrid = CenteredGrid(2,5)
my_font = pygame.font.Font(None, 30)

text = my_font.render("testing", 30, Config.BLACK)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    

    # print(testGrid.VScalars)
    # screen.fill(Config.WHITE) 
    for x in range(255):
        rect = pygame.Rect(x*(Config.SCREENWIDTH/255), 0, 1*(Config.SCREENWIDTH/255), Config.SCREENHEIGHT)
        pygame.draw.rect(screen, (x,255,255), rect, 1)
    screen.blit(text, (100,100))
    pygame.display.flip()
    screen.fill(Config.WHITE)

    # Cap the frame rate
    clock.tick()

# Quit Pygame
pygame.quit()
