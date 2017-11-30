"""
 Pygame base template for opening a window
 
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 
 Explanation video: http://youtu.be/vRB_983kUMc
"""
 
import pygame
import math
import ezgo
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)
 
pygame.init()
 
# Set the width and height of the screen [width, height]
WIDTH = 700
HEIGHT = 500
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("My Game")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Make specific game objects
background = pygame.image.load("map.png")
block = ezgo.Block(background, WIDTH / 2, HEIGHT / 2)
viewport = ezgo.Viewport(screen, block, background, (700, 500))

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    #Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
 
    # --- Game logic should go here

    pressed = pygame.key.get_pressed()
    dy = 0
    dx = 0
    if pressed[pygame.K_UP]:
        dy = -5
    if pressed[pygame.K_DOWN]:
        dy = 5
    if pressed[pygame.K_RIGHT]:
        dx = 5
    if pressed[pygame.K_LEFT]:
        dx = -5

    block.move(dx,dy)
        
    # --- Screen-clearing code goes here
 
    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
 
    # If you want a background image, replace this clear with blit'ing the
    # background image.
    screen.fill(WHITE)
 
    # --- Draw background
    viewport.draw()

    # --- Draw foreground
    viewport.draw_sprite()

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()
