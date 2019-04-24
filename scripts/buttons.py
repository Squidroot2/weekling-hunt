import pygame
from scripts import my_globals as g


class Button:
    def __init__(self, text, center, isBottom):
        # text is a string, center is a tuple, and isBottom is a boolean
        self.bg_color = g.WHITE
        self.txt_color = g.BLACK
        self.border_color = g.LIGHT_GRAY
        self.text = text
        self.isBottom = isBottom
        if isBottom:
            width = g.WINDOW_WIDTH / 6
            height = g.WINDOW_HEIGHT /8
            self.font =g.MAIN_FONT
        else:
            width = g.WINDOW_WIDTH /12
            height = g.WINDOW_HEIGHT / 16
            self.font= g.S_BUTTON_FONT

        self.rect = pygame.Rect(0,0,width,height)
        self.rect.center = (center)
        self.border = self.rect.copy()

    def draw(self):
        text_surf = (self.font.render(self.text, True, self.txt_color, self.bg_color))
        text_surf_rect = text_surf.get_rect()
        text_surf_rect.center = self.rect.center

        pygame.draw.rect(g.screen, self.bg_color, self.rect, 0)
        pygame.draw.rect(g.screen, self.border_color, self.border, 3)
        g.screen.blit(text_surf, text_surf_rect)

    def checkHover(self, mouse):
        # mouse is a two item tuple containing the x and y of the cursor
        if self.rect.collidepoint(mouse[0], mouse[1]):
            self.bg_color = g.LIGHT_GRAY
            self.border_color = g.BLACK
            return True
        else:
            self.bg_color = g.WHITE
            self.border_color = g.LIGHT_GRAY
            return False

def getButtons(game_state, bottom_pane, center_pane):

    misc_button_width = center_pane.width / 8
    misc_button_height = center_pane.height / 15

    # Draws the buttons to the screen and returns rectangle of the buttons
    if game_state == g.MAIN:
        choices = [g.STR_HUNT, g.STR_TRAIN, g.STR_SLEEP]
    elif game_state == g.BATTLE:
        choices = [g.STR_ATTACK, g.STR_FLEE]
    elif game_state == g.TRAIN:
        choices = [g.STR_STRENGTH, g.STR_AGILITY, g.STR_ACCURACY, g.STR_BACK]

    pane_divider = len(choices)+1

    buttons = []

    for i, choice in enumerate(choices, 1):
        center_of_button =((bottom_pane.width / pane_divider) * (i), bottom_pane.centery)
        button = Button(choice, center_of_button, True)
        buttons.append(button)


    # Buttons in the center pane
    help_button = Button(g.STR_HELP, (center_pane.left+center_pane.width/3, 25), False)
    retire_button = Button(g.STR_RETIRE, (center_pane.right-center_pane.width/3, 25), False)
    buttons.append(help_button)
    buttons.append(retire_button)

    return buttons


def getPromptButtons(askConfirm, bottom_pane):
    # These are only used for the pop-up prompts
    # isConfirm is a boolean, if true, there are two choices: confirm or back. Otherwise, the only choice is continue

    if askConfirm == True:
        choices = [g.STR_CONFIRM, g.STR_BACK]
    else:
        choices = [g.STR_CONTINUE]

    pane_divider = len(choices)+1

    buttons = []

    for i, choice in enumerate(choices, 1):
        center_of_button =((bottom_pane.width / pane_divider) * (i), bottom_pane.centery)
        button = Button(choice, center_of_button, True)
        buttons.append(button)

    return buttons