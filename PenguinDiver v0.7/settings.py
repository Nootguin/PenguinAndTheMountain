# Window
TITLE = "The Penguin and the Mountain"
WIDTH = 480
HEIGHT = 600
FPS = 60
FONT_NAME = 'arial'

HS_FILE = "highscore.txt"
SPRITESHEET = "spritesheet_jumper.png"

# Colours
WHITE =("#FFFFFF")
BLACK =("#000000")
SEA =("#3A72AE")
BEIGE =("#B9B770")

# Player Properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAVITY = 0.5
PLAYER_JUMP = 15

# Blocks - X, Y, Width, Height
BLOCK_LIST = [(0, HEIGHT - 40, WIDTH, 40), # floor
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 30),
                 (125, HEIGHT - 350, 100, 30),
                 (350, 200, 100, 30),
                 (175, 100, 50, 30)]

