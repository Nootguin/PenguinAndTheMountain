# Penguin Diver - platformer game
import pygame as pg
import random
from settings import *
from sprites import *
from os import path 


class Game:
    def __init__(self): # Initalises the game window
        pg.init() # runs pygame
        pg.mixer.init() # initalises sound
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE) # Sets Window Name
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME) # finds the closest match to that font name
        self.load_data()

    def load_data(self): # highscore, graphics and sound loading
        # Highscore loading
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, HS_FILE), 'r+') as f: # in quotation marks is what you are doing to file e.g. w = write, r = read
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0 # does this if file is empty

    
    def new(self): # Starts a fresh game
        self.score = 0
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
        self.draw_text(str(self.score), 22, WHITE, WIDTH/2, 15)       
        pg.display.flip() # after drawing everything, flip the display

    def start_screen(self): # Start Screen
        self.screen.fill(SEA)
        self.draw_text(TITLE, 38, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("Move = Arrow Keys | Space = Jump", 22, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press any key to start", 22, WHITE, WIDTH/2, HEIGHT * 3/4)
        self.draw_text("High Score: "+str(self.highscore), 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        self.wait_for_key()

    def game_over_screen(self): # Game Over Screen
        if not self.running:
            return
        self.screen.fill(SEA)
        self.draw_text("GAME OVER", 38, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("Score: "+str(self.score), 22, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press any key to start again", 22, WHITE, WIDTH/2, HEIGHT * 3/4)
        if self.score > self.highscore: # new highscore
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE", 22, WHITE, WIDTH/2, HEIGHT/2 + 40)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)

        pg.display.flip()
        self.wait_for_key()

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


    