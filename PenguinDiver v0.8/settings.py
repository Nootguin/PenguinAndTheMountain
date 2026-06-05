# Window
TITLE = "The Penguin and the Mountain"
WIDTH = 480
HEIGHT = 600
FPS = 60
FONT_NAME = 'Trebuchet MS'

HS_FILE = "highscore.txt"
SPRITESHEET = "spritesheet_jumper.png" # platforms and enemies spritesheet
PENGUIN = "penguin.png" # player spritesheet

# Colours
WHITE =("#FFFFFF")
BLACK =("#000000")
SEA =("#3A72AE")
BEIGE =("#B9B770")

# Player Properties
PLAYER_ACC = 0.3
PLAYER_FRICTION = -0.05
PLAYER_GRAVITY = 0.6
PLAYER_JUMP = 20

# Blocks - X, Y, Width, Height
BLOCK_LIST = [(0, HEIGHT - 40), # floor
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4),
                 (125, HEIGHT - 350),
                 (350, 200),
                 (175, 100)]

