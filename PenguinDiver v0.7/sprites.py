# Sprites for game
import pygame as pg
from settings import * # importing the settings file
vec = pg.math.Vector2 # vector math import

class Spritesheet: # calsss for loading and reading spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()
    
    def get_image(self, x, y, width, height): # grabs image out of spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x, y, width, height)) # gets image
        image = pg.transform.scale(image, (width//2, height//2) ) # scales images and truncates the decimal
        return image
    
class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        # animation and player sprites
        self.walking = False
        self.jumping = False
        self.current_frame = 0 # current frame the animation is on
        self.last_update = 0 # keeps track of when the last animation update happened so all animations are visible to the player
        self.load_images()
        self.image = self.stand_frames[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        # player placement
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        # player attributes
        self.pos = vec(WIDTH / 2, HEIGHT / 2) # player position
        self.vel = vec(0,0) # player velocity
        self.acc = vec(0,0) # player aceleration

    def load_images(self):
        self.stand_frames = [self.game.spritesheet.get_image(690,406,120,201),self.game.spritesheet.get_image(614,1063,120,191)] # each line in the list is an individual frame of the animation
        for frame in self.stand_frames:
            frame.set_colorkey(BLACK)
        self.walk_frames_r = [self.game.spritesheet.get_image(678,860,120,201),self.game.spritesheet.get_image(692,1458,120,207)]
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
            self.walk_frames_l.append(pg.transform.flip(frame, True, False)) # flips right facing frames
        self.jump_frames = self.game.spritesheet.get_image(416,1660,150,181)
        self.jump_frames.set_colorkey(BLACK)
    


    def jump(self): # player jump function
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.blocks, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -PLAYER_JUMP

    def update(self):
        self.animate()
        self.acc = vec(0,PLAYER_GRAVITY) # player gravity takes the value from settings to change the gravity
        keystate = pg.key.get_pressed() # player controls
        if keystate[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keystate[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
        # Friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # Movement equations
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        # Adds the ability for the player to wrap around the the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        self.rect.center = self.pos

        self.rect.midbottom = self.pos # sets the calculation positon of the player to the mid bottom
    
    def animate(self):
        now = pg.time.get_ticks() # gets current time of game
        if not self.jumping and not self.walking:
            if now - self.last_update > 300: # animation speed in milliseconds
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.stand_frames)
                self.image = self.stand_frames[self.current_frame]
                bottom = self.rect.bottom
                self.image = self.stand_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        

class Block(pg.sprite.Sprite):
    def __init__(self, x, y, w, h): # self, x, y, width, height
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(BEIGE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y