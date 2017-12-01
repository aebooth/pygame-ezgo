import ezgo
import pygame

world = ezgo.World()
world.views["level1"] = pygame.image.load("map.png")
world.set_current_view("level1")
world.start()
