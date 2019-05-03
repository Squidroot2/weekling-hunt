# Weekling Hunt: Pygame Edition
# By Hayden Foley
# I originally created this game to help myself learn python and programming in general.
# After discovering pygame, I wanted to recreate this game with 2D graphics

import scripts.my_globals as g
from scripts.draw_wh import getPaneDimensions
from scripts.screens import titleScreen, showScore, trainScreen, battleScreen, mainGameMenu, getPlayerName
from scripts.timekeeper import GameTime
from scripts.scoreboard import Scoreboard


def main():

    g.initializeGlobals()

    titleScreen()
    panes = getPaneDimensions()
    player = getPlayerName()  # Generates the player object
    game_time = GameTime()
    if Scoreboard.checkExist():
        scoreboard = Scoreboard.load()
    else:
        scoreboard = Scoreboard()

    while True:
        game_state = "MAIN"
        while True:  # main game loop
            if game_time.timeOver() or game_state == "END":
                break
            elif game_state == "MAIN":
                game_state = mainGameMenu(player, game_state, game_time, panes)
            elif game_state == "BATTLE":
                game_state = battleScreen(player, game_state, game_time, panes)
            elif game_state == "TRAIN":
                game_state = trainScreen(player, game_state, game_time, panes)

        showScore(player, scoreboard)
        resetGame(player, game_time)

def resetGame(player, game_time):

    player.reset()
    game_time.reset()



if __name__ == '__main__':
    main()
