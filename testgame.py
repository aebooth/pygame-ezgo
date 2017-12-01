import ezgo
import pygame

world = ezgo.World()
world.views["level1"] = pygame.image.load("map.png")
world.viewport.set_view(world.views["level1"])
world.player_sprite.set_bounding_rect(world.current_view.get_rect())
world.start()
