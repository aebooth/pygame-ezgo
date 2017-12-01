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
            
    #elif pressed[K_DOWN]:
        #world.player_sprite.set_active_animation("move_down")
    if world.player_sprite.animation is not None:
        world.player_sprite.animate()

world = ezgo.World()
world.views["level1"] = pygame.image.load("map.png")
world.set_current_view("level1")

superblock = ezgo.Spritesheet("superblock.png",50,50,8)
superblock.add_sequence("move_right",0,2)
superblock.add_sequence("move_left",1,2)
superblock.add_sequence("move_up",2,2)
#superblock.add_sequence("move_down",3,2)

world.player_sprite.animations["move_right"] = ezgo.Animation(superblock.sequences["move_right"])
world.player_sprite.animations["move_left"] = ezgo.Animation(superblock.sequences["move_left"])
world.player_sprite.animations["move_up"] = ezgo.Animation(superblock.sequences["move_up"])
#world.player_sprite.animations["move_down"] = ezgo.Animation(superblock.sequences["move_down"])

world.handle_keypresses = handle_keypresses

world.start()
