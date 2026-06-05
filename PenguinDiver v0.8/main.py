# The Penguin and The Mountain - platformer game
# Player art by GrafxKid
# Platform and Enemy art by Kenny
# Menu music by TAD
# Game music by BonoboGames

import pygame as pg
import random
from settings import *
from sprites import *
from os import path 


class Game:
    def __init__(self): # Initalises the game window
        pg.mixer.pre_init(44100, -16, 2, 2048) # this reduces the delay between sound and actions taking place in game
        pg.mixer.init() # initalises sound
        pg.init() # runs pygame
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE) # Sets Window Name
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME) # finds the closest match to that font name
        self.load_data()

    def load_data(self): # highscore, graphics and sound loading
        # Highscore loading
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        with open(path.join(self.dir, HS_FILE), 'r+') as f: # in quotation marks is what you are doing to file e.g. w = write, r+ = read if not write
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0 # does this if file is empty
        # Spritesheet loading
        self.spritesheet1 = Spritesheet(path.join(img_dir, SPRITESHEET))
        self.spritesheet2 = Spritesheet(path.join(img_dir, PENGUIN))
        # Sound loading
        self.snd_dir = path.join(self.dir, 'snd')
        self.img_dir = path.join(self.dir, 'img')
        self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Jump1.wav'))

    
    def new(self): # Starts a fresh game
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.blocks = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for block in BLOCK_LIST:
            b = Block(self, *block) # The star explodes the list into its components
            self.all_sprites.add(b)
            self.blocks.add(b)
        pg.mixer.music.load(path.join(self.snd_dir, 'Background Music.ogg'))
        self.run()
    
    def run(self): # Runs the game Loop
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(500)

    def update(self): # Updates within the game loop
        self.all_sprites.update()
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.blocks, False) # checks collisions with platforms and jumping logic
            if hits:
                lowest = hits[0] # checks which platform is lowest
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.y < lowest.rect.centery: # checks if feet are high enough to reach the platform
                    self.player.pos.y = lowest.rect.top # places player at top of the lowest platfrom
                    self.player.vel.y = 0 # stops player from sinking into block
                    self.player.jumping = False # allows player to jump on a block

        # if player reaches top 1/4 of screen scroll
        if self.player.rect.top <= HEIGHT / 4:
            self.player.pos.y += max(abs(self.player.vel.y), 3) # whichever number is bigger it will scroll the screen
            for plat in self.blocks:
                plat.rect.y += abs(self.player.vel.y)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10 # adds 10 to score when platform despawns


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
            b = Block(self,random.randrange(0, WIDTH-width),random.randrange(-75, -30))
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
            if event.type == pg.KEYUP: # jump event
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()
            
    def draw(self): # Everything drawn within the game loop
        # Draw / render
        background = pg.image.load(path.join(self.img_dir, 'background.png')).convert()
        background_rect = background.get_rect()
        self.screen.blit(background, background_rect)
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect) # player will always be infront
        self.draw_text(str(self.score), 22, WHITE, WIDTH/2, 15)       
        pg.display.flip() # after drawing everything, flip the display

    def start_screen(self): # Start Screen
        pg.mixer.music.load(path.join(self.snd_dir, 'Menu Music.ogg'))
        pg.mixer.music.play(loops=-1)
        background = pg.image.load(path.join(self.img_dir, 'background.png')).convert()
        background_rect = background.get_rect()
        self.screen.blit(background, background_rect)
        self.draw_text(TITLE, 34, BLACK, WIDTH/2, HEIGHT/4)
        self.draw_text("Move = Arrow Keys | Space = Jump", 22, BLACK, WIDTH/2, HEIGHT/2)
        self.draw_text("Press any key to start", 22, BLACK, WIDTH/2, HEIGHT * 3/4)
        self.draw_text("High Score: "+str(self.highscore), 22, BLACK, WIDTH / 2, 15)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(300)

    def game_over_screen(self): # Game Over Screen
        if not self.running:
            return
        pg.mixer.music.load(path.join(self.snd_dir, 'Menu Music.ogg'))
        pg.mixer.music.play(loops=-1)
        background = pg.image.load(path.join(self.img_dir, 'background.png')).convert()
        background_rect = background.get_rect()
        self.screen.blit(background, background_rect)
        self.draw_text("GAME OVER", 34, BLACK, WIDTH/2, HEIGHT/4)
        self.draw_text("Score: "+str(self.score), 22, BLACK, WIDTH/2, HEIGHT/2)
        self.draw_text("Press any key to start again", 22, BLACK, WIDTH/2, HEIGHT * 3/4)
        if self.score > self.highscore: # new highscore
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE", 22, BLACK, WIDTH/2, HEIGHT/2 + 40)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score: " + str(self.highscore), 22, BLACK, WIDTH / 2, HEIGHT / 2 + 40)

        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(300)

    def wait_for_key(self): # waits for player to do an action
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT: # stops program
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


game = Game()
game.start_screen()
while game.running:
    game.new()
    game.game_over_screen()
pg.quit()


    