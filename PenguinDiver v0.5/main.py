# Penguin Diver - platformer game
import pygame as pg
import random
from settings import *
from sprites import *


class Game:
    def __init__(self): # Initalises the game window
        pg.init() # runs pygame
        pg.mixer.init() # initalises sound
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE) # Sets Window Name
        self.clock = pg.time.Clock()
        self.running = True
    
    def new(self): # Starts a fresh game
        self.all_sprites = pg.sprite.Group()
        self.blocks = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for block in BLOCK_LIST:
            b = Block(*block) # The star explodes the list into its components
            self.all_sprites.add(b)
            self.blocks.add(b)
        self.run()
    
    def run(self): # Runs the game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self): # Updates within the game loop
        self.all_sprites.update()
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.blocks, False) # checks collisions with platforms
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0 # stops player from sinking into block

        # if player reaches top 1/4 of screen scroll
        if self.player.rect.top <= HEIGHT / 4:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.blocks:
                plat.rect.y += abs(self.player.vel.y)
                if plat.rect.top >= HEIGHT:
                    plat.kill() 


        # Game Over Conditions
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10) # max function gives maximum of two numbers
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.blocks) == 0:
            self.playing = False

        # spawn new platforms to keep same number - x, y, width, height
        while len(self.blocks) < 7:
            width = random.randrange (50, 100)
            b = Block(random.randrange(0, WIDTH-width),random.randrange(-75, -30),width, 30)
            self.blocks.add(b)
            self.all_sprites.add(b)

 
    def events(self): # Events within the game loop
        for event in pg.event.get(): # enables closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN: # jump event
                if event.key == pg.K_SPACE:
                    self.player.jump()
            
    def draw(self): # Everything drawn within the game loop
        # Draw / render
        self.screen.fill(SEA)
        self.all_sprites.draw(self.screen)       
        pg.display.flip() # after drawing everything, flip the display

    def start_screen(self): 
        pass

    def game_over_screen(self):
        pass


game = Game()
game.start_screen()
while game.running:
    game.new()
    game.game_over_screen()
pg.quit()


    