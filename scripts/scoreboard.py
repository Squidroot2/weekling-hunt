from scripts import my_globals as g


class Scoreboard:
    num_rows = 10

    def __init__(self):
        self.scores =[('',0)]*self.num_rows

    def addScore(self, score):
        pass

    def order(self, score):
        pass

    def draw(self):

        title_text = g.MAIN_FONT.render("High Scores", True, g.BLACK)
        title_text_rect = title_text.get_rect()
        title_text_rect.center = (g.WINDOW_WIDTH/2, g.MAIN_FONT.get_linesize())

        g.screen.blit(title_text, title_text_rect)


        linesize = g.SCORE_FONT.get_linesize()
        for i, score in enumerate(self.scores, 1):
            name_text = g.SCORE_FONT.render("%d. %s" %(i, score[0]), True, g.BLACK)
            name_text_rect = name_text.get_rect()
            name_text_rect.center = (g.WINDOW_WIDTH/5, (title_text_rect.bottom*2) + linesize*1.5*i)

            score_text = g.SCORE_FONT.render(str(score[1]), True, g.BLACK)
            score_text_rect = score_text.get_rect()
            score_text_rect.center = (g.WINDOW_WIDTH*4/5, name_text_rect.centery)

            g.screen.blit(name_text, name_text_rect)
            g.screen.blit(score_text, score_text_rect)





