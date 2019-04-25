import pygame
from scripts import my_globals as g


def drawMainScreen(panes, player, game_time, buttons):
    game_state = g.MAIN

    createMainTemplate(panes)
    drawStatValues(player, panes[g.LEFT])
    drawInfoPane(player, panes[g.RIGHT])
    drawCenterPane(game_state, game_time, panes[g.CENTER])
    drawButtons(buttons)

def drawBattleScreen(panes, player, buttons, enemy):
    createMainTemplate(panes)
    drawStatValues(player, panes[g.LEFT])
    drawStatValues(enemy, panes[g.RIGHT])
    drawEnemy(panes[g.CENTER], enemy)
    drawButtons(buttons)
    #todo write function that shows damage amounts on the side panes



def createMainTemplate(panes):
    # Creates the template that it used for all game g.screens. Does not update the g.screen
    g.screen.fill(g.WHITE)

    # Bottom Pane
    pygame.draw.rect(g.screen, g.BLACK, (panes[g.BOTTOM]), 0)
    pygame.draw.rect(g.screen, g.BLACK, (panes[g.LEFT]), 2)
    pygame.draw.rect(g.screen, g.BLACK, (panes[g.RIGHT]), 2)
    pygame.draw.rect(g.screen, g.BLACK, (panes[g.CENTER]), 2)


def drawStatValues(player, pane):

    # fills the left or right with player or enemy stats
    X_MARGIN = 30
    Y_MARGIN = 50

    name_text = g.MAIN_FONT.render(player.name, True, g.BLACK)
    name_text_rect = name_text.get_rect()
    name_text_rect.midleft = (pane.left+X_MARGIN, Y_MARGIN)

    health_text = g.STAT_FONT.render("Health:", True, g.BLACK)
    health_text_rect = health_text.get_rect()
    health_text_rect.midleft = (pane.left + X_MARGIN, name_text_rect.bottom + g.MAIN_FONT_SIZE * 2)

    health_value = g.STAT_FONT.render(("%d/%d" %(player.current_health,player.max_health)), True, g.BLACK)
    health_value_rect = health_value.get_rect()
    health_value_rect.midright = (pane.right-X_MARGIN, health_text_rect.centery)

    strength_text = g.STAT_FONT.render("Strength:", True, g.BLACK)
    strength_text_rect = strength_text.get_rect()
    strength_text_rect.midleft = (pane.left + X_MARGIN, health_text_rect.bottom + g.STAT_FONT_SIZE * 1.5)

    strength_value = g.STAT_FONT.render(str(player.strength), True, g.BLACK)
    strength_value_rect = strength_value.get_rect()
    strength_value_rect.midright = (pane.right-X_MARGIN, strength_text_rect.centery)

    agility_text = g.STAT_FONT.render("Agility:", True, g.BLACK)
    agility_text_rect = agility_text.get_rect()
    agility_text_rect.midleft = (pane.left + X_MARGIN, strength_text_rect.bottom + g.STAT_FONT_SIZE * 1.5)

    agility_value = g.STAT_FONT.render(str(player.agility), True, g.BLACK)
    agility_value_rect = agility_value.get_rect()
    agility_value_rect.midright = (pane.right-X_MARGIN, agility_text_rect.centery)

    accuracy_text = g.STAT_FONT.render("Accuracy:", True, g.BLACK)
    accuracy_text_rect = accuracy_text.get_rect()
    accuracy_text_rect.midleft = (pane.left + X_MARGIN, agility_text_rect.bottom + g.STAT_FONT_SIZE * 1.5)

    accuracy_value = g.STAT_FONT.render(str(player.accuracy), True, g.BLACK)
    accuracy_value_rect = accuracy_value.get_rect()
    accuracy_value_rect.midright = (pane.right-X_MARGIN, accuracy_text_rect.centery)

    gold_text = g.STAT_FONT.render("Gold:", True, g.BLACK)
    gold_text_rect = gold_text.get_rect()
    gold_text_rect.midleft = (pane.left + X_MARGIN, accuracy_text_rect.bottom + g.STAT_FONT_SIZE * 1.5)

    gold_value = g.STAT_FONT.render(str(player.gold), True, g.BLACK)
    gold_value_rect = gold_value.get_rect()
    gold_value_rect.midright = (pane.right-X_MARGIN, gold_text_rect.centery)

   # message_text = g.MESSAGE_FONT.render(player.message, True, g.BLACK)
   # message_text_rect = message_text.get_rect()
   # message_text_rect.midbottom = (pane.centerx, pane.bottom-g.MESSAGE_FONT_SIZE)

    g.screen.blit(name_text, name_text_rect)
    g.screen.blit(health_text, health_text_rect)
    g.screen.blit(strength_text, strength_text_rect)
    g.screen.blit(agility_text, agility_text_rect)
    g.screen.blit(accuracy_text, accuracy_text_rect)
    g.screen.blit(gold_text, gold_text_rect)
    g.screen.blit(health_value, health_value_rect)
    g.screen.blit(strength_value, strength_value_rect)
    g.screen.blit(agility_value, agility_value_rect)
    g.screen.blit(accuracy_value, accuracy_value_rect)
    g.screen.blit(gold_value, gold_value_rect)
    #g.screen.blit(message_text, message_text_rect)


def drawInfoPane(player, pane):

    # Draws the information in the right pane while in the main game g.screen

    total_gold_text = g.STAT_FONT.render("Total Goal Earned:", True, g.BLACK)
    total_gold_text_rect = total_gold_text.get_rect()
    total_gold_text_rect.midtop = (pane.centerx, pane.top + g.STAT_FONT_SIZE * 2)

    total_gold_value = g.STAT_FONT.render(str(player.total_gold), True, g.BLACK)
    total_gold_value_rect = total_gold_value.get_rect()
    total_gold_value_rect.midtop = (pane.centerx, total_gold_text_rect.bottom + g.STAT_FONT_SIZE)

    enemies_killed_text = g.STAT_FONT.render("Enemies Killed:", True, g.BLACK)
    enemies_killed_text_rect = enemies_killed_text.get_rect()
    enemies_killed_text_rect.midbottom = (pane.centerx, total_gold_value_rect.bottom + g.STAT_FONT_SIZE * 2)

    enemies_killed_value = g.STAT_FONT.render(str(player.enemies_killed), True, g.BLACK)
    enemies_killed_value_rect = enemies_killed_value.get_rect()
    enemies_killed_value_rect.midtop = (pane.centerx, enemies_killed_text_rect.bottom + g.STAT_FONT_SIZE)

    rare_killed_text = g.STAT_FONT.render("Rare Enemies Killed:", True, g.BLACK)
    rare_killed_text_rect = rare_killed_text.get_rect()
    rare_killed_text_rect.midbottom = (pane.centerx, enemies_killed_value_rect.bottom + g.STAT_FONT_SIZE * 2)

    rare_killed_value = g.STAT_FONT.render(str(player.rare_killed), True, g.BLACK)
    rare_killed_value_rect = rare_killed_value.get_rect()
    rare_killed_value_rect.midtop = (pane.centerx, rare_killed_text_rect.bottom + g.STAT_FONT_SIZE)

    g.screen.blit(total_gold_text, total_gold_text_rect)
    g.screen.blit(total_gold_value, total_gold_value_rect)
    g.screen.blit(enemies_killed_text, enemies_killed_text_rect)
    g.screen.blit(enemies_killed_value, enemies_killed_value_rect)
    g.screen.blit(rare_killed_text, rare_killed_text_rect)
    g.screen.blit(rare_killed_value, rare_killed_value_rect)


def drawCenterPane(game_state, game_time, pane): #todo center images for training

    if game_state == g.MAIN:
        if game_time.time == 0:  # time is morning
            center_image = pygame.image.load('./images/morning_bg.png').convert()
        elif game_time.time == 1:  # time is afternoon
            center_image = pygame.image.load('./images/midday_bg.png').convert()
        elif game_time.time == 2:  # time is evening
            center_image = pygame.image.load('./images/evening_bg.png').convert()
        elif game_time.time == 3:  # time is night
            center_image = pygame.image.load('./images/night_bg.png').convert()

    center_image = pygame.transform.smoothscale(center_image, (pane.width, pane.height))
    g.screen.blit(center_image, pane)

    time_and_day = ("%s %s" %(game_time.days_of_week[game_time.day], game_time.times_of_day[game_time.time]))

    time_text = g.STAT_FONT.render(time_and_day, True, g.BLACK)
    time_text_rect = time_text.get_rect()
    time_text_rect.center = (pane.centerx, pane.bottom - 30)

    g.screen.blit(time_text, time_text_rect)


def drawButtons(buttons):
    # buttons is a list of button objects
    for button in buttons:
        button.draw()


def drawBottomPane(bottom_pane):
    # blacks out the bottom pane. Not typically nessary unless it already has contents
    pygame.draw.rect(g.screen, g.BLACK, (bottom_pane), 0)


def drawPrompt(center_pane, message):
    # draws a prompt on the center of the center pane
    message_text = g.MESSAGE_FONT.render(message, True, g.BLACK,g.WHITE)
    message_text_rect = message_text.get_rect()
    message_text_rect.center = center_pane.center

    #draws a border around the prompt
    pygame.draw.rect(g.screen, g.BLACK, message_text_rect, 4)
    #blits prompt text to screen
    g.screen.blit(message_text, message_text_rect)

def drawEnemy(center_pane, enemy): #todo write draw enemy function
    pass


def getPaneDimensions():
    # Returns the rect dimensions left, center, right, and bottom pane
    bottom_pane_height = g.WINDOW_HEIGHT / 4
    side_pane_width = g.WINDOW_WIDTH / 4

    bottom_pane = pygame.Rect(0, bottom_pane_height * 3, g.WINDOW_WIDTH, bottom_pane_height)

    # The left and right panes are slightly offset to compensate for the thickness of the border
    left_pane = pygame.Rect(0,0,side_pane_width,bottom_pane_height*3)
    right_pane = pygame.Rect(g.WINDOW_WIDTH - side_pane_width, 0, side_pane_width, bottom_pane_height * 3)

    center_pane = pygame.Rect(side_pane_width, 0, g.WINDOW_WIDTH / 2, g.WINDOW_HEIGHT * 3 / 4)

    return left_pane, center_pane, right_pane, bottom_pane