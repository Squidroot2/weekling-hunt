import pygame
import os.path
from scripts import my_globals as g
from scripts.chargen import Player



def drawMainScreen(panes, player, game_time, buttons):
    # draws the training or main game screen
    game_state = g.MAIN

    createMainTemplate(panes)
    drawStatValues(player, panes['left'])
    drawInfoPane(player, panes['right'])
    drawCenterPane(game_state, game_time, panes['center'])
    drawButtons(buttons)

def drawBattleScreen(panes, player, buttons, enemy, player_damage, enemy_damage):
    createMainTemplate(panes)
    drawStatValues(player, panes['left'])
    drawStatValues(enemy, panes['right'])
    if enemy.image:
        drawEnemy(panes['center'], enemy)
    drawButtons(buttons)
    
    if not player_damage == None:
        drawDamageDone(panes['right'], player_damage)
        
    if not enemy_damage == None:
        drawDamageDone(panes['left'], enemy_damage)

def drawHelpScreen(buttons):
    g.screen.fill(g.WHITE)
    drawButtons(buttons)
    
    help_title = g.TITLE_FONT.render("How To Play", True, g.BLACK)
    help_title_rect = help_title.get_rect()
    help_title_rect.midtop = (g.WINDOW_WIDTH/2, g.WINDOW_HEIGHT/50)
    
    message = []
    message.append("")
    message.append("The object of the game is to have as much gold as possible by the end of the week.")
    message.append("There are 7 days in the week(Sunday-Saturday) and 4 times of day(Morning, Mid-day, Evening, Night)")
    message.append("Earn gold by defeating enemies in battle. The tougher the enemy, the more gold you earn")
    message.append("Tougher enemies come out in the evening with the toughest enemies coming out late night")
    message.append("You can spend your gold on training your skills to defeat more difficult enemies.")
    message.append("Training costs more gold as you increase your stats.")
    message.append("Sleep to fully heal your health. Sleeping always brings you to the next morning regardless of what time of day it is")
    message.append("")
    message.append("Strength is the maximum damage than you can do")
    message.append("Agility determines first strike and dodge chance")
    message.append("Accuracy affects chance to hit and chance to deal maximum damage")
    
    for i,line in enumerate(message):
        line_text = g.MESSAGE_FONT.render(line, True, g.BLACK)
        line_text_rect = line_text.get_rect()
        line_text_rect.midtop = (g.WINDOW_WIDTH/2, help_title_rect.bottom + (g.MAIN_FONT_SIZE*1.5*i))
        
        g.screen.blit(line_text, line_text_rect)    
    
    g.screen.blit(help_title, help_title_rect)

def createMainTemplate(panes):
    # Creates the template that it used for all game g.screens. Does not update the g.screen
    g.screen.fill(g.WHITE)

    # Bottom Pane
    pygame.draw.rect(g.screen, g.BLACK, (panes['bottom']), 0)
    pygame.draw.rect(g.screen, g.BLACK, (panes['left']), 2)
    pygame.draw.rect(g.screen, g.BLACK, (panes['right']), 2)
    pygame.draw.rect(g.screen, g.BLACK, (panes['center']), 2)


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
    
    # Make Player's Health red when low
    if isinstance(player, Player) and player.current_health <= 5:
        health_color = g.RED
    else:
        health_color = g.BLACK

    health_value = g.STAT_FONT.render(("%d/%d" %(player.current_health,player.max_health)), True, health_color)
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

    if game_state == g.MAIN or game_state == g.TRAIN:
        if game_time.time == 0:  # time is morning
            image_path = os.path.join('images', 'morning_bg.png')
        elif game_time.time == 1:  # time is afternoon
            image_path = os.path.join('images', 'midday_bg.png')
        elif game_time.time == 2:  # time is evening
            image_path = os.path.join('images', 'evening_bg.png')
        elif game_time.time == 3:  # time is night
            image_path = os.path.join('images', 'night_bg.png')

    center_image = pygame.image.load(image_path).convert()
    center_image = pygame.transform.smoothscale(center_image, (pane.width, pane.height))
    g.screen.blit(center_image, pane)

    time_and_day = (str(game_time))

    time_text = g.MAIN_FONT.render(time_and_day, True, g.BLACK)
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
    enemy_image = pygame.transform.smoothscale(enemy.image, (center_pane.width, center_pane.height))
    g.screen.blit(enemy_image, center_pane)


def getPaneDimensions():
    # Returns the rect dimensions left, center, right, and bottom pane
    bottom_pane_height = g.WINDOW_HEIGHT / 4
    side_pane_width = g.WINDOW_WIDTH / 4

    bottom_pane = pygame.Rect(0, bottom_pane_height * 3, g.WINDOW_WIDTH, bottom_pane_height)

    # The left and right panes are slightly offset to compensate for the thickness of the border
    left_pane = pygame.Rect(0,0,side_pane_width,bottom_pane_height*3)
    right_pane = pygame.Rect(g.WINDOW_WIDTH - side_pane_width, 0, side_pane_width, bottom_pane_height * 3)

    center_pane = pygame.Rect(side_pane_width, 0, g.WINDOW_WIDTH / 2, g.WINDOW_HEIGHT * 3 / 4)

    return {'left': left_pane, 'center': center_pane, 'right': right_pane, 'bottom': bottom_pane}

def drawScoreScreen(player):
    if player.alive:
        g.screen.fill(g.GOLD)
        win_text = g.TITLE_FONT.render("You Survived the Week!", True, g.BLACK)
        win_text_rect = win_text.get_rect()
        win_text_rect.center = (g.WINDOW_WIDTH/2, g.WINDOW_HEIGHT/3)
        
        score_text = g.TITLE_FONT.render("You finished the week with %d gold" % player.gold, True, g.BLACK)
        score_text_rect = score_text.get_rect()
        score_text_rect.center = (g.WINDOW_WIDTH/2, g.WINDOW_HEIGHT*2/3)
        
        g.screen.blit(win_text, win_text_rect)
        g.screen.blit(score_text, score_text_rect)      
        
    else:
        g.screen.fill(g.RED)
        death_text = g.TITLE_FONT.render("You have died and lost all of your gold", True, g.BLACK)
        death_text_rect = death_text.get_rect()
        death_text_rect.center = (g.WINDOW_WIDTH/2, g.WINDOW_HEIGHT/2)
        
        g.screen.blit(death_text, death_text_rect)
        
def drawDamageDone(pane, damage_done):

    # player_damage is damge inflicted by the player on the enemy, enemy_damge is inverse
    
    if damage_done == 0:
        message = "MISS"
    else: 
        message = "-%d" % damage_done
            
    message_text = g.TITLE_FONT.render(message, True, g.BLACK)
    message_text_rect = message_text.get_rect()
    message_text_rect.center = (pane.centerx, pane.height *5/6)
        
    g.screen.blit(message_text, message_text_rect)
    
   
        
        
        