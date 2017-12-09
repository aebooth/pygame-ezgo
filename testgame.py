import ezgo
import pygame

def handle_keypresses():
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_RIGHT]:
        if world.player_sprite.animation is world.player_sprite.animations["move_right"]:
            world.player_sprite.animate()
        else:
            world.player_sprite.set_active_animation("move_right")
            
    elif pressed[pygame.K_LEFT]:
        if world.player_sprite.animation is world.player_sprite.animations["move_left"]:
            world.player_sprite.animate()
        else:
            world.player_sprite.set_active_animation("move_left")
            
    elif pressed[pygame.K_UP]:
        if world.player_sprite.animation is world.player_sprite.animations["move_up"]:
            world.player_sprite.animate()
        else:
            world.player_sprite.set_active_animation("move_up")
            
    elif pressed[pygame.K_DOWN]:
        if world.player_sprite.animation is world.player_sprite.animations["move_down"]:
            world.player_sprite.animate()
        else:
            world.player_sprite.set_active_animation("move_down")

world = ezgo.World()
world.add_view("level1",pygame.image.load("map.png"),pygame.image.load("map_boundaries.png"))
world.set_current_view("level1")

superblock = ezgo.Spritesheet("aPiratedSpritesheet.png",64,64,0)
superblock.add_sequence("move_right",3,9)
superblock.add_sequence("move_left",1,9)
superblock.add_sequence("move_up",0,9)
superblock.add_sequence("move_down",2,9)

world.player_sprite.animations["move_right"] = ezgo.Animation(superblock.sequences["move_right"])
world.player_sprite.animations["move_left"] = ezgo.Animation(superblock.sequences["move_left"])
world.player_sprite.animations["move_up"] = ezgo.Animation(superblock.sequences["move_up"])
world.player_sprite.animations["move_down"] = ezgo.Animation(superblock.sequences["move_down"])

world.player_sprite.set_active_animation("move_down")

world.handle_keypresses = handle_keypresses

world.start()
