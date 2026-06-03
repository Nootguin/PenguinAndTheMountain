# Sprites for game
import pygame as pg
from settings import * # importing the settings file
vec = pg.math.Vector2 # vector math import

class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((30,40))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2) # player position
        self.vel = vec(0,0) # player velocity
        self.acc = vec(0,0) # player aceleration

    def update(self):
        self.acc = vec(0,0.01) # 0.01 here adds gravity going downwards
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
        

class Block(pg.sprite.Sprite):
    def __init__(self, x, y, w, h): # self, x, y, width, height
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(BEIGE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y