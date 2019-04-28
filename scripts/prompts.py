import pygame
from pygame.constants import MOUSEMOTION, MOUSEBUTTONUP

from scripts.quit import checkForQuit
from scripts import my_globals as g
from scripts.buttons import getPromptButtons
from scripts.draw_wh import drawBottomPane, drawPrompt, drawButtons


def confirmRetire(panes):
    #Return true or false
    message = "Are you sure you want to end the game?"
    return promptScreen(panes, message, True)


def confirmTrain(panes, skill, player):
    #Returns true or false
    message = "Are you sure you want to train %s for %d gold" % (skill, player.getSkillValue(skill))
    return promptScreen(panes, message, True)


def cannotTrainPrompt(panes, skill, player):
    if player.getSkillValue(skill) == 5:
        message = "Cannot train %s any further" % skill
    else:
        message = "Cannot train %s: not enough gold" % skill

    promptScreen(panes, message, False)


def promptScreen(panes, message, askConfirm):
    # Draws various prompts depending on the state of the game
    # message is what will be displayed. askConfirm is whether it is a yes/no prompt or a continue prompt

    drawBottomPane(panes['bottom'])
    drawPrompt(panes['center'], message)
    buttons = getPromptButtons(askConfirm, panes['bottom'])
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
                if button.text == g.STR_CONTINUE:
                    return True
                elif button.text == g.STR_CONFIRM:
                    return True
                elif button.text == g.STR_BACK:
                    return False

        drawButtons(buttons)
        g.FPS_CLOCK.tick(g.FPS)
        pygame.display.update()