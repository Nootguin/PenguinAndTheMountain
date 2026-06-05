# Sprites for game
import pygame as pg
from settings import * # importing the settings file
vec = pg.math.Vector2 # vector math import
import random
class Spritesheet: # calsss for loading and reading spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()
    
    def get_image(self, x, y, width, height): # grabs image out of spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x, y, width, height)) # gets image
        image = pg.transform.scale(image, (width//2, height//2) ) # scales images
        return image
    
    def get_player_image(self, x, y, width, height): # grabs image out of spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x, y, width, height)) # gets image
        image = pg.transform.scale(image, (width*4, height*4) ) # scales player
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
        self.pos = vec(40, HEIGHT - 100) # player start position
        self.vel = vec(0,0) # player velocity
        self.acc = vec(0,0) # player aceleration

    def load_images(self):
        self.stand_frames = [self.game.spritesheet2.get_player_image(4,75,16,16),self.game.spritesheet2.get_player_image(51,76,16,16)] # each line in the list is an individual frame of the animation
        for frame in self.stand_frames:
            frame.set_colorkey(BLACK)
        self.walk_frames_l = [self.game.spritesheet2.get_player_image(52,108,17,17),self.game.spritesheet2.get_player_image(75,11,17,17)]
        self.walk_frames_r = []
        for frame in self.walk_frames_l:
            frame.set_colorkey(BLACK)
            self.walk_frames_r.append(pg.transform.flip(frame, True, False)) # flips right facing frames
        self.jump_frames = self.game.spritesheet2.get_player_image(28,76,16,17)
        self.jump_frames.set_colorkey(BLACK)
    
    def jump_cut(self):
        if self.jumping and self.vel.y < 0:
            self.vel.y *= 0.5

    def jump(self): # player jump function
        self.rect.x += 2 # number of pixels above the ground the player can jump
        hits = pg.sprite.spritecollide(self, self.game.blocks, False)
        self.rect.x -= 2
        if hits and not self.jumping:
            self.game.jump_sound.play() # plays jump sound
            self.jumping = True
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
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        # Movement equations
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        # Adds the ability for the player to wrap around the the screen
        if self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width / 2

        self.rect.midbottom = self.pos # sets the calculation positon of the player to the mid bottom of the player
    
    def animate(self):
        now = pg.time.get_ticks() # gets current time of game
        # checks if player is walking and if so plays the the animation
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        # walk animation
        if self.walking:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_r)
                bottom = self.rect.bottom
                if self.vel.x < 0: # if velocity is negative it uses the left frame else it uses the right frame
                    self.image = self.walk_frames_l[self.current_frame]
                else:
                    self.image = self.walk_frames_r[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom # fixes position of image

        if not self.jumping and not self.walking:
            if now - self.last_update > 600: # animation speed in milliseconds
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.stand_frames)
                self.image = self.stand_frames[self.current_frame]
                bottom = self.rect.bottom
                self.image = self.stand_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        

class Block(pg.sprite.Sprite):
    def __init__(self, game, x, y): # self, x, y, width, height
        pg.sprite.Sprite.__init__(self)
        self.game = game
        images = [self.game.spritesheet1.get_image(0,768,380,94),self.game.spritesheet1.get_image(0,480,380,94),self.game.spritesheet1.get_image(213,1764,201,100),self.game.spritesheet1.get_image(382,306,201,100)]
        self.image = random.choice(images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y