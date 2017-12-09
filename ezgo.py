import pygame
import numpy as np
import math

class World:
    def __init__(self,width=700,height=500,name="My Game"):
        pygame.init()
        self.pygame_window = pygame.display.set_mode((width,height))
        pygame.display.set_caption(name)
        self.views = {"blank":pygame.Surface((self.pygame_window.get_rect().width,self.pygame_window.get_rect().height))}
        self.current_view = self.views["blank"]
        self.internal_boundaries = {"blank":[[0 for x in range(width)] for x in range(height)]}
        self.current_internal_boundaries = self.internal_boundaries["blank"]
        self.background_items = pygame.sprite.Group()
        self.npc_sprites = pygame.sprite.Group()
        self.active_items = pygame.sprite.Group()
        self.foreground_items = pygame.sprite.Group()
        self.player_sprite = Sprite(self, 0,0)
        self.hud_view = Sprite(self,0,0,image=pygame.Surface((width,height)))
        self.hud_view.image.set_alpha(0)
        self.viewport = Viewport(self.current_view,self.pygame_window)
        self.running = False

    # don't override this!!!!
    def add_view(self,name,view,view_internal_boundaries=None):
        self.views[name] = view
        if view_internal_boundaries is None:
            self.internal_boundaries[name] = np.zeros((view.get_rect().height,view.get_rect().width))
        else:
            arr = np.zeros((view_internal_boundaries.get_rect().width,view_internal_boundaries.get_rect().height),np.int32)
            pygame.pixelcopy.surface_to_array(arr, view_internal_boundaries, 'G')
            arr = arr.T > 50
            self.internal_boundaries[name] = arr
    
    # don't override this
    def start(self):
        clock = pygame.time.Clock()
        self.running = True
        while self.running:
            self.pygame_window.fill((255,255,255))
            self.run()
            pygame.display.flip()
            clock.tick(60)
        pygame.quit()

    # only override this if you have a good reason to
    def handle_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    # override this
    def handle_keypresses(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_t]:
            print("pressing 't' for test works")

    # only override this if you have a good reason to
    def update_environment(self):
        self.background_items.update()
        self.npc_sprites.update()
        self.active_items.update()
        self.foreground_items.update()

    # don't override this 
    def update_player(self):
        self.player_sprite.update()

    # override this
    def handle_npc_interactions(self):
        npcs_hit = pygame.sprite.spritecollide(self.player_sprite,self.npc_sprites,dokill=False)
        for npc in npcs_hit:
            print("hit npc at " + str((npc.x,npc.y)))

    # override this
    def handle_active_item_interactions(self):
        active_items_hit = pygame.sprite.spritecollide(self.player_sprite, self.active_items, dokill=False)
        for active_item in active_items_hit:
            print("hit active_item at " + str((active_item.x, active_item.y)))

    # don't override this
    def update_hud(self):
        self.hud_view.update()

    # don't override this
    def update_viewport(self):
        self.viewport.center_horizontal_on(self.player_sprite)
        self.viewport.center_vertical_on(self.player_sprite)

    # don't override this
    # Warning: Fails Silently!
    def set_current_view(self,view_name):
        if view_name in self.views:
            self.current_view = self.views[view_name]
            self.current_internal_boundaries = self.internal_boundaries[view_name]
            self.viewport.set_view(self.current_view)

    # only override this if you have a good reason to
    def draw(self):
        #setup dummy view
        view = self.current_view.copy()
        # draw background_items
        self.background_items.draw(view)
        # draw npc_sprites
        self.npc_sprites.draw(view)
        # draw active_items
        self.active_items.draw(view)
        # draw player_sprite
        self.player_sprite.draw(view)
        # draw foreground_items
        self.foreground_items.draw(view)
        # draw current compound view
        self.viewport.draw(view)
        # draw remaining HUD elements
        self.hud_view.draw(self.pygame_window)

    # only override this if you have a good reason to
    def run(self):
        self.handle_quit()
        self.handle_keypresses()
        self.update_player()
        self.update_environment()
        self.handle_npc_interactions()
        self.handle_active_item_interactions()
        self.update_hud()
        self.update_viewport()
        self.draw()
        

class Sprite(pygame.sprite.Sprite):
    def __init__(self, world, x=0, y=0, animation=None, image=pygame.Surface((50,50))):
        pygame.sprite.Sprite.__init__(self)
        self.animations = {"default":animation}
        self.animation = self.animations["default"]
        self.image = image
        self.x = x
        self.y = y
        #The Sprite's rect represents its position in the viewport, not the world
        self.rect = pygame.Rect(self.x,self.y,self.image.get_rect().width,self.image.get_rect().height)
        self.world = world

    # don't override this
    def move(self,dx,dy):
        destx = self.x + dx
        desty = self.y + dy
        # Check moves against the view's outside boundaries
        xmax =self.world.current_view.get_rect().width - self.rect.width
        ymax = self.world.current_view.get_rect().height - self.rect.height
        
        if destx < 0:
            destx = 0
        elif destx > xmax:
            destx = xmax

        if desty < 0:
            desty = 0
        elif desty > ymax:
            desty = ymax

        # Check moves against the view's internal boundaries
        chunk = self.world.current_internal_boundaries[desty:desty + self.rect.height,destx:destx + self.rect.width]
        if np.all(chunk):
            self.x = destx
            self.y = desty



    # don't override this
    # WARNING: Fails silently!!
    def set_active_animation(self, animation_name):
        if animation_name in self.animations:
            self.animation = self.animations[animation_name]
            self.image = self.animation.get_frame()

    # don't override this
    def animate(self):
        self.animation.advance()
        self.image = self.animation.get_frame()

    # don't override this
    def draw(self, view):
        view.blit(self.image,(self.x,self.y))

    # override this
    def update(self):
        pressed = pygame.key.get_pressed()
        dy = 0
        dx = 0
        if pressed[pygame.K_UP]:
            dy = -2
        if pressed[pygame.K_DOWN]:
            dy = 2
        if pressed[pygame.K_RIGHT]:
            dx = 2
        if pressed[pygame.K_LEFT]:
            dx = -2
        self.move(dx,dy)

class Viewport:
    def __init__(self,view,screen):
        self.view = view
        self.screen = screen
        self.width = self.screen.get_rect().width
        self.height = self.screen.get_rect().height
        self.xmax = self.view.get_rect().width-self.width
        self.ymax = self.view.get_rect().height-self.height
        self.rect = pygame.Rect(0, 0, self.width, self.height)

    def get_rect(self):
        return self.rect

    def set_view(self, view):
        self.view = view
        self.xmax = self.view.get_rect().width - self.width
        self.ymax = self.view.get_rect().height - self.height

    def set_position(self,x,y):
        if x < 0:
            self.rect.x = 0
        elif x <= self.xmax:
            self.rect.x = x
        else:
            self.rect.x = self.xmax

        if y < 0:
            self.rect.y = 0
        elif y <= self.ymax:
            self.rect.y = y
        else:
            self.rect.y = self.ymax

    def center_horizontal_on(self,sprite):
        destx = sprite.x + sprite.rect.width//2 - self.width//2
        if destx < 0:
            self.rect.x = 0
        elif destx <= self.xmax:
            self.rect.x = destx
        else:
            self.rect.x = self.xmax

    def center_vertical_on(self, sprite):
        desty = sprite.y + sprite.rect.height//2 - self.height//2
        if desty < 0:
            self.rect.y = 0
        elif desty <= self.ymax:
            self.rect.y = desty
        else:
            self.rect.y = self.ymax

    def draw(self,view):
        self.screen.blit(view.subsurface(self.rect),self.screen.get_rect())

class Spritesheet:
    def __init__(self,file_path,sprite_width,sprite_height,sprite_padding=0):
        self.sheet = pygame.image.load(file_path)
        self.sheet.convert()
        self.padding = sprite_padding
        self.sprite_rect = pygame.Rect(self.padding,self.padding,sprite_width,sprite_height)
        self.sequences = {}

    def add_sequence(self,name,start_row,num_frames):
        self.sprite_rect.y = start_row * (self.padding + self.sprite_rect.height)
        self.sprite_rect.x = self.padding
        frames = []
        for i in range(num_frames):
            frames.append(self.sheet.subsurface(self.sprite_rect))
            self.sprite_rect.move_ip(self.padding + self.sprite_rect.width , 0)
        self.sequences[name] = frames

class Animation:
    def __init__(self,frame_sequence):
        self.frames = frame_sequence
        self.current_frame = 0
        # Number of frames to wait before advancing
        self.advance_rate = 1
        self.frame_counter = 0

    def get_frame(self):
        return self.frames[self.current_frame]

    def advance(self):
        if self.frame_counter < self.advance_rate:
            self.frame_counter = self.frame_counter + 1
        else:
            self.current_frame = self.current_frame + 1
            if self.current_frame >= len(self.frames):
                self.current_frame = 0
            self.frame_counter = 0

