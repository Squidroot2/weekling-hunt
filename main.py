# Weekling Hunt: Pygame Edition
# By Hayden Foley
# I orginally created this game to help myself learn python and programming in general.
# After discovering pygame, I wanted to recreate this game with 2D graphics

import random, sys, pygame
import chargen
from pygame.locals import *   # Import Constants


FPS = 60
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# Colors         R    G    B
WHITE        = (255, 255, 255)
BLACK        = (  0,   0,   0)
SKY_BLUE     = (  0, 213, 255)


#Font sizes
TITLE_FONT_SIZE = 48
MAIN_FONT_SIZE = 30
STAT_FONT_SIZE = 24

# SYNTACTIC SUGAR for PANES # Returns the rect dimensions left, center, right, and bottom pane
LEFT = 0
CENTER = 1
RIGHT = 2
BOTTOM = 3


# Gamestates
START = 0
MAIN = 1
BATTLE = 2
TRAIN = 3
SLEEP = 4
END = 5


def main():
    global FPS_CLOCK, MAIN_FONT, TITLE_FONT, STAT_FONT, screen

    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Weekling Hunt')

    TITLE_FONT = pygame.font.Font('freesansbold.ttf', TITLE_FONT_SIZE)
    MAIN_FONT = pygame.font.Font('freesansbold.ttf', MAIN_FONT_SIZE)
    STAT_FONT = pygame.font.Font('freesansbold.ttf', STAT_FONT_SIZE)



    game_state = START
    game_state = titleScreen(game_state)

    game_time = GameTime()
    player = generatePlayer() # Generates the global variable player
    while True:  # main game loop
        checkForQuit()
        if game_state == MAIN:
            game_state = mainGameScreen(player, game_state, game_time)
        elif game_state == BATTLE:
            game_state = battleScreen()
        elif game_state == TRAIN:
            game_state = trainScreen()
        elif game_state == END:
            break

    showScore()


class GameTime:
    day = 0
    time = 0
    days_of_week = ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')
    times_of_day = ('Morning', 'Afternoon', 'Evening', 'Night')
    max_day = len(days_of_week)

    def incrementTime(self):
        self.time += 1
        if self.time == len(self.times_of_day):
            self.incrementDay()

    def incrementDay(self):
        self.day += 1  # increases the day of the week
        self.time = 0  # sets time to morning
        
    def timeOver(self):
        if self.day == self.max_day:
            print("The week is over. Game Ended")
            print()
            return True
        else:
            return False


def titleScreen(game_state):
    screen.fill(SKY_BLUE)

    title = TITLE_FONT.render("Weekling Adventure", True, BLACK)
    title_rect = title.get_rect()
    title_rect.center = (WINDOW_WIDTH /2, WINDOW_HEIGHT / 6)

    subtitle1 = MAIN_FONT.render("A Game By Hayden Foley", True, BLACK)
    subtitle1_rect = subtitle1.get_rect()
    subtitle1_rect.midtop = (WINDOW_WIDTH/2, title_rect.bottom+MAIN_FONT_SIZE)

    subtitle2 = MAIN_FONT.render("With Art By Nina Langlois", True, BLACK)
    subtitle2_rect = subtitle2.get_rect()
    subtitle2_rect.midtop = (WINDOW_WIDTH/2, subtitle1_rect.bottom)

    continue_prompt = MAIN_FONT.render("Press Enter to Continue", True, BLACK)
    continue_prompt_rect = continue_prompt.get_rect()
    continue_prompt_rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT * 2/3)


    screen.blit(title, title_rect)
    screen.blit(subtitle1, subtitle1_rect)
    screen.blit(subtitle2, subtitle2_rect)
    screen.blit(continue_prompt, continue_prompt_rect)

    while game_state == START:
        checkForQuit()
        for event in pygame.event.get(KEYUP):
            if event.key == K_RETURN:
                game_state += 1
                return game_state

        pygame.display.update()
        FPS_CLOCK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
       if event.key == K_ESCAPE:
          terminate() # terminate if the KEYUP event was for the Esc key
       pygame.event.post(event) # put the other KEYUP event objects back


def generatePlayer():
    player_name = getPlayerName()
    player = chargen.Player(player_name)
    return player


def getPlayerName():
    prompt = MAIN_FONT.render("What is your name?", True, BLACK)
    prompt_rect = prompt.get_rect()
    prompt_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - (MAIN_FONT_SIZE*2))

    continue_prompt = MAIN_FONT.render("Press Enter to Continue", True, BLACK)
    continue_prompt_rect = continue_prompt.get_rect()
    continue_prompt_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT *2/3)

    name = ''
    pygame.event.clear()  # Needed to make sure that any keys hit in the title screen don't end up in the name
    while True:
        screen.fill(SKY_BLUE)
        screen.blit(prompt, prompt_rect)

        checkForQuit()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RETURN and not name == '':
                    return name
                elif event.key == K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode

        input = MAIN_FONT.render(name, True, BLACK)
        input_rect = input.get_rect()
        input_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

        if len(name) > 0:
            screen.blit(input, input_rect)
            screen.blit(continue_prompt, continue_prompt_rect)

        FPS_CLOCK.tick(FPS)
        pygame.display.update()


def getPaneDimensions():
    # Returns the rect dimensions left, center, right, and bottom pane
    BOTTOM_PANE_HEIGHT = WINDOW_HEIGHT/4
    SIDE_PANE_WIDTH = WINDOW_WIDTH/4

    bottom_pane = pygame.Rect(0, BOTTOM_PANE_HEIGHT*3, WINDOW_WIDTH, BOTTOM_PANE_HEIGHT)

    # The left and right panes are slightly offset to compensate for the thickness of the border
    left_pane = pygame.Rect(0,0,SIDE_PANE_WIDTH,BOTTOM_PANE_HEIGHT*3)
    right_pane = pygame.Rect(WINDOW_WIDTH-SIDE_PANE_WIDTH, 0,SIDE_PANE_WIDTH,BOTTOM_PANE_HEIGHT*3)

    center_pane = pygame.Rect(SIDE_PANE_WIDTH,0,WINDOW_WIDTH/2,WINDOW_HEIGHT*3/4)

    return left_pane, center_pane, right_pane, bottom_pane


def createMainTemplate(panes): #todo finish making template
    # Creates the template that it used for all game screens. Does not update the screen
    screen.fill(WHITE)
    

    #Bottom Pane
    pygame.draw.rect(screen, BLACK, (panes[BOTTOM]), 0)
    pygame.draw.rect(screen, BLACK, (panes[LEFT]), 2)
    pygame.draw.rect(screen, BLACK, (panes[RIGHT]), 2)
    pygame.draw.rect(screen, BLACK, (panes[CENTER]), 2)


def drawStatValues(player, pane):
    #fills the left or right with player or enemy stats
    X_MARGIN = 30
    Y_MARGIN = 50
    
    name_text = MAIN_FONT.render(player.name, True, BLACK)
    name_text_rect = name_text.get_rect()
    name_text_rect.midleft = (pane.left+X_MARGIN, Y_MARGIN)

    health_text = STAT_FONT.render("Health:", True, BLACK)
    health_text_rect = health_text.get_rect()
    health_text_rect.midleft = (pane.left+X_MARGIN, name_text_rect.bottom + MAIN_FONT_SIZE*2)

    health_value = STAT_FONT.render(("%d/%d" %(player.current_health,player.max_health)), True, BLACK)
    health_value_rect = health_value.get_rect()
    health_value_rect.midright = (pane.right-X_MARGIN, health_text_rect.centery)

    strength_text = STAT_FONT.render("Strength:", True, BLACK)
    strength_text_rect = strength_text.get_rect()
    strength_text_rect.midleft = (pane.left+X_MARGIN, health_text_rect.bottom + STAT_FONT_SIZE*1.5)

    strength_value = STAT_FONT.render(str(player.strength), True, BLACK)
    strength_value_rect = strength_value.get_rect()
    strength_value_rect.midright = (pane.right-X_MARGIN, strength_text_rect.centery)

    agility_text = STAT_FONT.render("Agility:", True, BLACK)
    agility_text_rect = agility_text.get_rect()
    agility_text_rect.midleft = (pane.left+X_MARGIN, strength_text_rect.bottom + STAT_FONT_SIZE*1.5)

    agility_value = STAT_FONT.render(str(player.agility), True, BLACK)
    agility_value_rect = agility_value.get_rect()
    agility_value_rect.midright = (pane.right-X_MARGIN, agility_text_rect.centery)

    accuracy_text = STAT_FONT.render("Accuracy:", True, BLACK)
    accuracy_text_rect = accuracy_text.get_rect()
    accuracy_text_rect.midleft = (pane.left+X_MARGIN, agility_text_rect.bottom + STAT_FONT_SIZE*1.5)

    accuracy_value = STAT_FONT.render(str(player.accuracy), True, BLACK)
    accuracy_value_rect = accuracy_value.get_rect()
    accuracy_value_rect.midright = (pane.right-X_MARGIN, accuracy_text_rect.centery)
    
    gold_text = STAT_FONT.render("Gold:", True, BLACK)
    gold_text_rect = gold_text.get_rect()
    gold_text_rect.midleft = (pane.left+X_MARGIN, accuracy_text_rect.bottom + STAT_FONT_SIZE*1.5)
    
    gold_value = STAT_FONT.render(str(player.gold), True, BLACK)
    gold_value_rect = gold_value.get_rect()
    gold_value_rect.midright = (pane.right-X_MARGIN, gold_text_rect.centery)

    screen.blit(name_text, name_text_rect)
    screen.blit(health_text, health_text_rect)
    screen.blit(strength_text, strength_text_rect)
    screen.blit(agility_text, agility_text_rect)
    screen.blit(accuracy_text, accuracy_text_rect)
    screen.blit(gold_text, gold_text_rect)
    screen.blit(health_value, health_value_rect)
    screen.blit(strength_value, strength_value_rect)
    screen.blit(agility_value, agility_value_rect)
    screen.blit(accuracy_value, accuracy_value_rect)
    screen.blit(gold_value, gold_value_rect)


def drawInfoPane(player, pane):
    #Draws the information in the right pane while in the main game screen
    
    total_gold_text = STAT_FONT.render("Total Goal Earned:", True, BLACK)
    total_gold_text_rect = total_gold_text.get_rect()
    total_gold_text_rect.midtop = (pane.centerx, pane.top + STAT_FONT_SIZE*2)
    
    total_gold_value = STAT_FONT.render(str(player.total_gold), True, BLACK)
    total_gold_value_rect = total_gold_value.get_rect()
    total_gold_value_rect.midtop = (pane.centerx, total_gold_text_rect.bottom + STAT_FONT_SIZE)
    
    enemies_killed_text = STAT_FONT.render("Enemies Killed:", True, BLACK)
    enemies_killed_text_rect = enemies_killed_text.get_rect()
    enemies_killed_text_rect.midbottom = (pane.centerx, total_gold_value_rect.bottom + STAT_FONT_SIZE*2)
    
    enemies_killed_value = STAT_FONT.render(str(player.enemies_killed), True, BLACK)
    enemies_killed_value_rect = enemies_killed_value.get_rect()
    enemies_killed_value_rect.midtop = (pane.centerx, enemies_killed_text_rect.bottom + STAT_FONT_SIZE)
    
    rare_killed_text = STAT_FONT.render("Rare Enemies Killed:", True, BLACK)
    rare_killed_text_rect = rare_killed_text.get_rect()
    rare_killed_text_rect.midbottom = (pane.centerx, enemies_killed_value_rect.bottom + STAT_FONT_SIZE*2)
    
    rare_killed_value = STAT_FONT.render(str(player.rare_killed), True, BLACK)
    rare_killed_value_rect = rare_killed_value.get_rect()
    rare_killed_value_rect.midtop = (pane.centerx, rare_killed_text_rect.bottom + STAT_FONT_SIZE)
        
    screen.blit(total_gold_text, total_gold_text_rect)
    screen.blit(total_gold_value, total_gold_value_rect)
    screen.blit(enemies_killed_text, enemies_killed_text_rect)
    screen.blit(enemies_killed_value, enemies_killed_value_rect)
    screen.blit(rare_killed_text, rare_killed_text_rect)
    screen.blit(rare_killed_value, rare_killed_value_rect)


def drawCenterPane(game_state, game_time, pane): #todo add other center images

    if game_state == MAIN:
        if game_time.time == 0:  # time is morning
            center_image = pygame.image.load('./images/morning_center.png').convert()
        elif game_time == 1:  # time is afternoon
            pass
        elif game_time == 2:  # time is evening
            pass
        elif game_time == 3:  # time is night
            pass

    center_image = pygame.transform.smoothscale(center_image, (pane.width, pane.height))
    screen.blit(center_image, pane)        
        
    
def showScore(): #todo write showScore function
    pass


def trainScreen(): #todo write trainScreen function
    pass


def battleScreen(): #todo write battleScreen function
    pass


def mainGameScreen(player, game_state, game_time): #todo write mainGameScreen function
    panes = getPaneDimensions()
    createMainTemplate(panes)
    drawStatValues(player, panes[LEFT])
    drawInfoPane(player, panes[RIGHT])
    drawCenterPane(game_state, game_time, panes[CENTER])
    while True:
        checkForQuit()
        FPS_CLOCK.tick(FPS)
        pygame.display.update()


if __name__ == '__main__':
    main()