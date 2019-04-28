import pygame, os
from pygame.locals import *

from scripts import my_globals as g
from scripts.buttons import getButtons, getHelpButtons
from scripts.draw_wh import drawMainScreen, drawButtons, drawBattleScreen, drawScoreScreen, drawHelpScreen
from scripts.prompts import confirmRetire, confirmTrain, cannotTrainPrompt, promptScreen
from scripts.quit import checkForQuit
from scripts.chargen import generateEnemy, Player, getEnemyDataFrom



def titleScreen():
    g.screen.fill(g.SKY_BLUE)

    title = g.TITLE_FONT.render("Weekling Hunt", True, g.BLACK)
    title_rect = title.get_rect()
    title_rect.center = (g.WINDOW_WIDTH / 2, g.WINDOW_HEIGHT / 6)

    subtitle1 = g.MAIN_FONT.render("A Game By Hayden Foley", True, g.BLACK)
    subtitle1_rect = subtitle1.get_rect()
    subtitle1_rect.midtop = (g.WINDOW_WIDTH / 2, title_rect.bottom + g.MAIN_FONT_SIZE)

    subtitle2 = g.MAIN_FONT.render("With Art By Nina Langlois", True, g.BLACK)
    subtitle2_rect = subtitle2.get_rect()
    subtitle2_rect.midtop = (g.WINDOW_WIDTH / 2, subtitle1_rect.bottom)

    continue_prompt = g.MAIN_FONT.render("Press Enter to Continue", True, g.BLACK)
    continue_prompt_rect = continue_prompt.get_rect()
    continue_prompt_rect.center = (g.WINDOW_WIDTH / 2, g.WINDOW_HEIGHT * 2 / 3)

    g.screen.blit(title, title_rect)
    g.screen.blit(subtitle1, subtitle1_rect)
    #g.screen.blit(subtitle2, subtitle2_rect)
    g.screen.blit(continue_prompt, continue_prompt_rect)

    title = True

    while title:
        checkForQuit()
        for event in pygame.event.get(KEYUP):
            if event.key == K_RETURN:
                title = False

        pygame.display.update()
        g.FPS_CLOCK.tick(g.FPS)


def getPlayerName():
    prompt = g.MAIN_FONT.render("What is your name?", True, g.BLACK)
    prompt_rect = prompt.get_rect()
    prompt_rect.center = (g.WINDOW_WIDTH / 2, g.WINDOW_HEIGHT / 2 - (g.MAIN_FONT_SIZE * 2))

    continue_prompt = g.MAIN_FONT.render("Press Enter to Continue", True, g.BLACK)
    continue_prompt_rect = continue_prompt.get_rect()
    continue_prompt_rect.center = (g.WINDOW_WIDTH / 2, g.WINDOW_HEIGHT * 2 / 3)

    name = ''
    pygame.event.clear()  # Needed to make sure that any keys hit in the title Screen don't end up in the name
    while True:
        g.screen.fill(g.SKY_BLUE)
        g.screen.blit(prompt, prompt_rect)

        checkForQuit()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RETURN and not name == '':
                    return Player(name)
                elif event.key == K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode

        input = g.MAIN_FONT.render(name, True, g.BLACK)
        input_rect = input.get_rect()
        input_rect.center = (g.WINDOW_WIDTH / 2, g.WINDOW_HEIGHT / 2)

        if len(name) > 0:
            g.screen.blit(input, input_rect)
            g.screen.blit(continue_prompt, continue_prompt_rect)

        g.FPS_CLOCK.tick(g.FPS)
        pygame.display.update()


def showScore(player):  # todo write showScore function

    end = True

    drawScoreScreen(player)

        
    while end:
        checkForQuit()
        for event in pygame.event.get(KEYUP):
            if event.key == K_RETURN:
                end = False

        pygame.display.update()
        g.FPS_CLOCK.tick(g.FPS)


def trainScreen(player, game_state, game_time, panes):

    buttons = getButtons(game_state, panes['bottom'], panes['center'])
    drawMainScreen(panes, player, game_time, buttons)

    mousex, mousey = 0, 0

    while True:

        mouse_clicked = False
        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mouse_clicked = True

        for button in buttons:
            over_button = button.checkHover((mousex,mousey))

            if over_button and mouse_clicked:  # Button has been clicked
                if button.text == g.STR_BACK:
                    return "MAIN"
                elif button.text == g.STR_RETIRE:
                    confirm = confirmRetire(panes)
                    if confirm:
                        return "END"
                    else:
                        drawMainScreen(panes, player, game_time, buttons)
                if button.text in (g.STR_STRENGTH, g.STR_AGILITY, g.STR_ACCURACY):
                    if player.canTrain(button.text):
                        if confirmTrain(panes, button.text, player):
                            player.trainSkill(button.text)
                            game_time.incrementTime()
                            return "MAIN"
                        else:
                            drawMainScreen(panes, player, game_time, buttons)
                    else:
                        cannotTrainPrompt(panes, button.text, player)
                        drawMainScreen(panes, player, game_time, buttons)





        drawButtons(buttons)
        g.FPS_CLOCK.tick(g.FPS)
        pygame.display.update()


def battleScreen(player, game_state, game_time, panes):  # todo write battleScreen function
    buttons = getButtons(game_state, panes['bottom'], panes['center'])
    enemy = generateEnemy(game_time)

    mousex, mousey = 0, 0

    drawBattleScreen(panes, player, buttons, enemy, None, None)
    # First strike
    if enemy.agility > player.agility:
        enemy_damage = enemy.attack(player)
        drawBattleScreen(panes, player, buttons, enemy, None, enemy_damage)
        
        message = "The %s strikes first due to its superior agility" %enemy.name
        promptScreen(panes, message, False)
        
        # If first strike killed the player
        if not player.alive:
            message = "You have been killed by the %s" % enemy.name
            promptScreen(panes, message, False)
            return "END"
        
        else:
            drawBattleScreen(panes, player, buttons, enemy, None, None)

    while True: # mainGameMenu loop

        mouse_clicked = False  # every loop mouse clicked is set to false until mousebuttonup event occurs
        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mouse_clicked = True

        for button in buttons:
            over_button = button.checkHover((mousex,mousey))

            if over_button and mouse_clicked:  # Button has been clicked
                if button.text == g.STR_ATTACK:
                    player_damage = player.attack(enemy)
                    
                    if enemy.alive:  # Enemy is still alive after player attacks
                        enemy_damage = enemy.attack(player)  # Enemy attacks player
                        
                        if not player.alive: # If player is now dead, return end game state
                            drawBattleScreen(panes, player, buttons, enemy, player_damage, enemy_damage)
                            message = "You have been killed by the %s" % enemy.name
                            promptScreen(panes, message, False)
                            return "END"
                        else:
                            # After a trade of blows, redraws battle panes to keep track of health.
                            drawBattleScreen(panes, player, buttons, enemy, player_damage, enemy_damage)  
                            
                            
                    else:  # If the enemy is dead, player collects gold adds kill to count. Then main game state is returned
                        player.collect_gold(enemy)
                        player.killedEnemy(enemy)
                        drawBattleScreen(panes, player, buttons, enemy, player_damage, None)
                        message = "You have killed the %s and earned %d gold" % (enemy.name, enemy.gold)
                        promptScreen(panes, message, False)
                        game_time.incrementTime()
                        return "MAIN"


                elif button.text == g.STR_FLEE:
                    message = "Are you sure you want to flee from the %s" % enemy.name
                    confirm = promptScreen(panes, message, True)
                    if confirm:
                        game_time.incrementTime()
                        return "MAIN"
                    else:
                        drawBattleScreen(panes, player, buttons, enemy)
                elif button.text == g.STR_RETIRE:
                    if confirmRetire(panes):
                        return "END"
                    else:
                        drawBattleScreen(panes, player, buttons, enemy)
                elif button.text == g.STR_HELP:
                    # show help stuff
                    pass

        drawButtons(buttons)
        g.FPS_CLOCK.tick(g.FPS)
        pygame.display.update()


def helpScreen():
    
    csvfile = os.path.join('data', 'enemies.csv')
    enemy_list = getEnemyDataFrom(csvfile)
    buttons = getHelpButtons("BOTTOM", enemy_list)

    
    drawHelpScreen(buttons)
    
    mousex, mousey = 0, 0
    
    layer = 1
    while layer > 0: # help screen loop

        mouse_clicked = False  # every loop mouse clicked is set to false until mousebuttonup event occurs
        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mouse_clicked = True

        for button in buttons:
            over_button = button.checkHover((mousex,mousey))

            if over_button and mouse_clicked:  # Button has been clicked
                # Back goes up a layer
                if button.text == g.STR_BACK:
                    layer -= 1
                    
        drawButtons(buttons)
        g.FPS_CLOCK.tick(g.FPS)
        pygame.display.update()
    
def mainGameMenu(player, game_state, game_time, panes):

    buttons = getButtons(game_state, panes['bottom'], panes['center'])
    drawMainScreen(panes, player, game_time, buttons) # calls a bunch of draw functions from draw_wh

    mousex, mousey = 0, 0

    while True: # mainGameMenu loop

        mouse_clicked = False  # every loop mouse clicked is set to false until mousebuttonup event occurs
        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mouse_clicked = True

        for button in buttons:
            over_button = button.checkHover((mousex,mousey))

            if over_button and mouse_clicked:  # Button has been clicked
                if button.text == g.STR_HUNT:
                    return "BATTLE"
                elif button.text == g.STR_TRAIN:
                    return "TRAIN"
                elif button.text == g.STR_SLEEP:
                    message = "Sleep until tomorrow morning to heal?"
                    confirm = promptScreen(panes, message, True)
                    if confirm:
                        player.sleep()
                        game_time.incrementDay()
                    return "MAIN"
                elif button.text == g.STR_RETIRE:
                    if confirmRetire(panes):
                        return "END"
                    else:
                        drawMainScreen(panes, player, game_time, buttons)
                elif button.text == g.STR_HELP:
                    helpScreen()
                    drawMainScreen(panes, player, game_time, buttons)

        drawButtons(buttons)
        g.FPS_CLOCK.tick(g.FPS)
        pygame.display.update()