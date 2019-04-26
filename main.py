# Weekling Hunt: Pygame Edition
# By Hayden Foley
# I originally created this game to help myself learn python and programming in general.
# After discovering pygame, I wanted to recreate this game with 2D graphics

import scripts.my_globals as g
from scripts.draw_wh import getPaneDimensions
from scripts.screens import titleScreen, showScore, trainScreen, battleScreen, mainGameMenu, getPlayerName
from scripts.timekeeper import GameTime



def main():

    g.initializeGlobals()

    game_state = g.START
    game_state = titleScreen(game_state)
    game_time = GameTime()

    player = getPlayerName() # Generates the global variable player
    panes = getPaneDimensions()
    while True:  # main game loop
        if game_time.timeOver():
            game_state = g.END
            break
            
        if game_state == g.MAIN:
            game_state = mainGameMenu(player, game_state, game_time, panes)
        elif game_state == g.BATTLE:
            game_state = battleScreen(player, game_state, game_time, panes)
        elif game_state == g.TRAIN:
            game_state = trainScreen(player, game_state, game_time, panes)
        elif game_state == g.END:
            break

    showScore(player)


if __name__ == '__main__':
    main()
