import pygame
import math

class World:
    def __init__(self,width=700,height=500,name="My Game"):
        pygame.init()
        self.pygame_window = pygame.display.set_mode((width,height))
        pygame.display.set_caption(name)
        self.views = {"blank":pygame.Surface((self.pygame_window.get_rect().width,self.pygame_window.get_rect().height))}
        self.background_items = pygame.sprite.Group()
        self.npc_sprites = pygame.sprite.Group()
        self.active_items = pygame.sprite.Group()
        self.foreground_items = pygame.sprite.Group()
        self.player_sprite = Sprite(width//2,height//2)
        self.hud_view = Sprite(0,0,pygame.Surface(width,height))
        self.viewport = Viewport(self.views["blank"],self.pygame_window)
        self.running = False

    # don't override this
    def start(self):
        self.running = True
        while self.running:
            self.__run__()

    # maybe override this
    def handle_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    # override this
    def handle_keypresses(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_t]:
            print("pressing 't' for test works")

    def update_environment(self):
        self.background_items.update()
        self.npc_sprites.update()
        self.active_items.update()
        self.foreground_items.update()

    def update_player(self):
        self.player_sprite.update()

    # override this if you want to do anything other than stop the sprite on collision
    def ensure_move_validity(self,dx,dy):
        # This method is a turd to figure out!
        self.player_sprite.move(dx,dy)
        self.player_sprite.calculate_rect(self.viewport)
        active_items_hit = pygame.sprite.spritecollide(self.player_sprite,self.active_items,dokill=False)
        if len(active_items_hit) > 0:
            self.player_sprite.move(-dx,-dy)
            self.player_sprite.calculate_rect(self.viewport)

    # override this
    def handle_npc_interactions(self):
        npcs_hit = pygame.sprite.spritecollide(self.player_sprite,self.npc_sprites,dokill=False)
        for npc in npcs_hit:
            print("hit npc at " + str((npc.x,npc.y)))

    def handle_active_item_interactions(self):
        active_items_hit = pygame.sprite.spritecollide(self.player_sprite, self.active_items, dokill=False)
        for active_item in active_items_hit:
            print("hit active_item at " + str((active_item.x, active_item.y)))

    def update_hud(self):
        self.hud_view.update()

    # maybe override this
    def draw(self):
        # draw current view
        self.viewport.draw()
        # draw background_items
        self.background_items.draw(self.pygame_window)
        # draw npc_sprites
        self.npc_sprites.draw(self.pygame_window)
        # draw active_items
        self.active_items.draw(self.pygame_window)
        # draw player_sprite
        self.player_sprite.draw(self.pygame_window)
        # draw foreground_items
        self.foreground_items.draw(self.pygame_window)
        # draw remaining HUD elements
        self.hud_view.draw(self.pygame_window)

    #
    def __run__(self):
        self.handle_quit()
        self.handle_keypresses()
        self.update_player()
        self.update_environment()
        self.handle_npc_interactions()
        self.handle_active_item_interactions()
        self.update_environment() # YES--I did mean to do this twice!
        self.update_player() # YES--I did mean to do this twice
        self.update_hud()
        self.draw()

class Sprite(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, animation=None, image=pygame.Surface((50,50)).fill((255,0,0)), bounding_rect=None):
        pygame.sprite.Sprite.__init__(self)
        self.animations = {}
        self.animations["default"] = animation
        self.animation = self.animations["default"]
        self.image = image
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x,self.y,self.image.get_rect().width,self.image.get_rect().height)
        self.bounding_rect = bounding_rect
        if bounding_rect is not None:
            self.xmax = bounding_rect.width
            self.ymax = bounding_rect.height
        else:
            self.xmax = None
            self.ymax = None

    def move(self,dx,dy):
        if self.bounding_rect != None:
            destx = self.x + dx
            if destx < 0:
                self.x = 0
            elif destx <= self.xmax:
                self.x = destx
            else:
                self.x = self.xmax

            desty = self.y + dy
            if desty < 0:
                self.y = 0
            elif desty <= self.ymax:
                self.y = desty
            else:
                self.y = self.ymax
        else:
            self.x = self.x + dx
            self.y = self.x + dx

    def set_bounds(self,bounding_rect):
        self.bounding_rect = bounding_rect
        if bounding_rect is not None:
            self.xmax = bounding_rect.width
            self.ymax = bounding_rect.height

    def calculate_rect(self,viewport=None):
        if viewport is not None:
            self.rect = pygame.Rect(self.x,self.y,self.image.get_rect().width,self.image.get_rect().height).clip(viewport.get_rect())
        else:
            self.rect = pygame.Rect(self.x,self.y,self.image.get_rect().width,self.image.get_rect().height)
        return self.rect

    # WARNING: Fails silently!!
    def set_active_animation(self, animation_name):
        if animation_name in self.animations.keys():
            self.animation = self.animations[animation_name]
            self.image = self.animation.get_frame()

    def animate(self):
        self.animation.advance()
        self.image = self.animation.get_frame()

    def draw(self, screen):
        screen.blit(self.image,self.rect)

    def update(self):
        pass

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
        destx = sprite.rect.x + sprite.rect.width//2 - self.width//2
        if destx < 0:
            self.rect.x = 0
        elif destx <= self.xmax:
            self.rect.x = destx
        else:
            self.rect.x = self.xmax

    def center_vertical_on(self, sprite):
        desty = sprite.rect.y + sprite.rect.height//2 - self.height//2
        if desty < 0:
            self.rect.y = 0
        elif desty <= self.ymax:
            self.rect.y = desty
        else:
            self.rect.y = self.ymax

    def draw(self):
        self.screen.blit(self.view.subsurface(self.rect),self.screen.get_rect())

class Spritesheet:
    def __init__(self,file_path,sprite_width,sprite_height,sprite_padding=0):
        self.sheet = pygame.image.load(file_path)
        self.padding = sprite_padding
        self.sprite_rect = pygame.Rect(sprite_padding,sprite_padding,sprite_width,sprite_height)
        self.sequences = {}

    def add_sequence(self,name,start_row,num_frames):
        self.sprite_rect.y = self.sprite_rect.y + start_row * (self.padding + self.sprite_rect.height)
        frames = []
        for i in range(num_frames):
            frames.append(self.sheet.subsurface(self.sprite_rect))
            self.sprite_rect.move(self.padding + self.sprite_rect.width , 0)
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
        if self.frame_counter >= self.advance_rate:
            self.current_frame = self.current_frame + 1
            if self.current_frame >= len(self.frames):
                self.current_frame = 0
            self.frame_counter = 0
        else:
            self.frame_counter = self.frame_counter + 1