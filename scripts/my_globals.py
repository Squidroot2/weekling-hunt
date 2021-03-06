import pygame

# contains global variables that are used throughout the program

def initializeGlobals(): # todo turn this into a class
    global FPS, WINDOW_WIDTH, WINDOW_HEIGHT, \
        WHITE, BLACK, SKY_BLUE, LIGHT_GRAY, RED, GOLD, \
        TITLE_FONT_SIZE, MAIN_FONT_SIZE, STAT_FONT_SIZE, S_BUTTON_FONT_SIZE, MESSAGE_FONT_SIZE, \
        FPS_CLOCK, MAIN_FONT, TITLE_FONT, STAT_FONT, S_BUTTON_FONT, MESSAGE_FONT, SCORE_FONT, screen, \
        STR_HUNT, STR_TRAIN, STR_SLEEP, STR_HELP, STR_RETIRE, STR_ATTACK, STR_FLEE, \
        STR_STRENGTH, STR_AGILITY, STR_ACCURACY, STR_BACK, STR_CONFIRM, STR_CONTINUE 

    # Screen Info
    FPS = 60
    WINDOW_WIDTH = 1280
    WINDOW_HEIGHT = 720

    # Colors         R    G    B
    WHITE =        (255, 255, 255)
    BLACK =        (  0,  0,    0)
    SKY_BLUE =     (  0, 213, 255)
    LIGHT_GRAY =   (200, 200, 200)
    RED =          (255,   0,   0)
    GOLD =         (255, 215, 100)

    # Font sizes
    TITLE_FONT_SIZE = 48
    MAIN_FONT_SIZE = 30
    STAT_FONT_SIZE = 24
    S_BUTTON_FONT_SIZE = 18
    MESSAGE_FONT_SIZE = 20
    SCORE_FONT_SIZE = 30
    
    #Button texts
    STR_HUNT = "Hunt"
    STR_TRAIN = "Train"
    STR_SLEEP = "Sleep"
    STR_HELP = "HELP"
    STR_RETIRE = "RETIRE"
    STR_ATTACK = "Attack"
    STR_FLEE = "Flee"
    STR_STRENGTH = "Strength"
    STR_AGILITY = "Agility"
    STR_ACCURACY = "Accuracy"
    STR_BACK = "Back"
    STR_CONFIRM = "Confirm"
    STR_CONTINUE = "CONTINUE"
    
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Weekling Hunt')

    TITLE_FONT = pygame.font.Font('freesansbold.ttf', TITLE_FONT_SIZE)
    MAIN_FONT = pygame.font.Font('freesansbold.ttf', MAIN_FONT_SIZE)
    STAT_FONT = pygame.font.Font('freesansbold.ttf', STAT_FONT_SIZE)
    S_BUTTON_FONT = pygame.font.Font('freesansbold.ttf', S_BUTTON_FONT_SIZE)
    MESSAGE_FONT = pygame.font.Font('freesansbold.ttf', MESSAGE_FONT_SIZE)
    SCORE_FONT = pygame.font.Font('freesansbold.ttf', SCORE_FONT_SIZE)
    
