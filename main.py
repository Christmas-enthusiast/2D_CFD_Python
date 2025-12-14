import pygame
import sys

def main():
    # Initialize Pygame
    pygame.init()

    # Screen settings
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("My Pygame Boilerplate")

    # Clock for controlling frame rate
    clock = pygame.time.Clock()
    FPS = 60

    # Game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Add other event handling (e.g., keyboard/mouse input) here

        # Game logic and updates
        # ...

        # Drawing
        screen.fill((30, 30, 30)) # Fill the screen with a dark gray color
        # Add drawing code here (e.g., blitting images, drawing shapes)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

    # Quit Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
