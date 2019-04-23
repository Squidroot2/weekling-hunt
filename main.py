# Weekling Hunt: Pygame Edition
# By Hayden Foley
# I originally created this game to help myself learn python and programming in general.
# After discovering pygame, I wanted to recreate this game with 2D graphics

import sys
from pygame.locals import *   # Import Constants

from scripts.draw_wh import *
from scripts.timekeeper import GameTime
from scripts import chargen
from scripts.buttons import *


def main():

    g.initializeGlobals()

    game_state = g.START
    game_state = titleScreen(game_state)
    game_time = GameTime()

    player = generatePlayer() # Generates the global variable player
    panes = getPaneDimensions()
    while True:  # main game loop
        checkForQuit()
        if game_time.timeOver():
            game_state = g.END

        if game_state == g.MAIN:
            game_state = mainGameMenu(player, game_state, game_time, panes)
        elif game_state == g.BATTLE:
            game_state = battleScreen(player, game_state, game_time, panes)
        elif game_state == g.TRAIN:
            game_state = trainScreen()
        elif game_state == g.END:
            break

    showScore()

def titleScreen(game_state):
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
    g.screen.blit(subtitle2, subtitle2_rect)
    g.screen.blit(continue_prompt, continue_prompt_rect)

    while game_state == g.START:
        checkForQuit()
        for event in pygame.event.get(KEYUP):
            if event.key == K_RETURN:
                game_state += 1
                return game_state

        pygame.display.update()
        g.FPS_CLOCK.tick(g.FPS)


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
    prompt = g.MAIN_FONT.render("What is your name?", True, g.BLACK)
    prompt_rect = prompt.get_rect()
    prompt_rect.center = (g.WINDOW_WIDTH / 2, g.WINDOW_HEIGHT / 2 - (g.MAIN_FONT_SIZE * 2))

    continue_prompt = g.MAIN_FONT.render("Press Enter to Continue", True, g.BLACK)
    continue_prompt_rect = continue_prompt.get_rect()
    continue_prompt_rect.center = (g.WINDOW_WIDTH / 2, g.WINDOW_HEIGHT * 2 / 3)

    name = ''
    pygame.event.clear()  # Needed to make sure that any keys hit in the title g.screen don't end up in the name
    while True:
        g.screen.fill(g.SKY_BLUE)
        g.screen.blit(prompt, prompt_rect)

        checkForQuit()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RETURN and not name == '':
                    return name
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


def showScore():  # todo write showScore function
    pass


def trainScreen():  # todo write trainScreen function
    pass


def battleScreen(player, game_state, game_time, panes):  # todo write battleScreen function
    buttons = getButtons(game_state, panes[g.BOTTOM], panes[g.CENTER])
    enemy = chargen.generateEnemy(game_time)

    mousex, mousey = 0, 0

    drawBattleScreen(panes, player, buttons, enemy)
    # First strike
    if enemy.agility > player.agility:
        message = "The %s strikes first due to its superior agility" %enemy.name
        promptScreen(panes, message, False)
        enemy.attack(player)

        # If first strike killed the player
        if not player.alive:
            message = "You have been killed by the %s" % enemy.name
            promptScreen(panes, message, False)
            return g.END

        else:
            drawBattleScreen(panes, player, buttons, enemy)

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
                if button.text == 'Attack':
                    player.attack(enemy)
                    if enemy.alive:  # Enemy is still alive after player attacks
                        enemy.attack(player)  # Enemy attacks player
                        if not player.alive: # If player is now dead, return end game state
                            message = "You have been killed by the %s" % enemy.name
                            promptScreen(panes, message, False)
                            return g.END
                        else:
                            drawBattleScreen(panes, player, buttons, enemy)  # After a trade of blows, redraws battle panes to keep track of health.
                    else:  # If the enemy is dead, player collects gold adds kill to count. Then main game state is returned
                        player.collect_gold(enemy)
                        player.killedEnemy(enemy)
                        drawBattleScreen(panes, player, buttons, enemy)
                        message = "You have killed the %s and earned %d gold" % (enemy.name, enemy.gold)
                        promptScreen(panes, message, False)
                        game_time.incrementTime()
                        return g.MAIN


                elif button.text == 'Flee':
                    message = "Are you sure you want to flee from the %s" % enemy.name
                    confirm = promptScreen(panes, message, True)
                    if confirm:
                        game_time.incrementTime()
                        return g.MAIN
                    else:
                        drawBattleScreen(panes, player, buttons, enemy)
                elif button.text == 'Retire':
                    message = "Are you sure you want to end the game?"
                    confirm = promptScreen(panes, message, True)
                    if confirm:
                        return g.END
                    else:
                        drawBattleScreen(panes, player, buttons, enemy)
                elif button.text == 'Help':
                    # show help stuff
                    pass

        drawButtons(buttons)
        g.FPS_CLOCK.tick(g.FPS)
        pygame.display.update()

def mainGameMenu(player, game_state, game_time, panes):  # todo finish mainScreen function

    buttons = getButtons(game_state, panes[g.BOTTOM], panes[g.CENTER])
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
                if button.text == 'Hunt':
                    return g.BATTLE
                elif button.text == 'Train':
                    return g.TRAIN
                elif button.text == 'Sleep':
                    message = "Sleep until tomorrow morning to heal?"
                    confirm = promptScreen(panes, message, True)
                    if confirm:
                        player.sleep()
                        game_time.incrementDay()
                    return g.MAIN
                elif button.text == 'Retire':
                    # confirm retire
                    pass
                elif button.text == 'Help':
                    # show help stuff
                    pass




        drawButtons(buttons)
        g.FPS_CLOCK.tick(g.FPS)
        pygame.display.update()


def promptScreen(panes, message, askConfirm):
    # Draws various prompts depending on the state of the game
    # message is what will be displayed. askConfirm is whether it is a yes/no prompt or a continue prompt

    drawBottomPane(panes[g.BOTTOM])
    drawPrompt(panes[g.CENTER], message)
    buttons = getPromptButtons(askConfirm, panes[g.BOTTOM])
    drawButtons(buttons)


    mousex, mousey = 0, 0

    while True: # loop

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
                if button.text == 'Continue':
                    return True
                elif button.text == 'Confirm':
                    return True
                elif button.text == 'Back':
                    return False

        drawButtons(buttons)
        g.FPS_CLOCK.tick(g.FPS)
        pygame.display.update()

if __name__ == '__main__':
    main()
