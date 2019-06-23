from scripts import my_globals as g
import os
import pickle

class Scoreboard:
    num_rows = 10
    file_location = os.path.join('data', 'scoreboard.sb')

    def __init__(self, name="High Scores"):
        self.scores =[('',0)]*self.num_rows
        self.newest_score = None
        self.name = name


    def addScore(self, new_score):
        place = None
        for i, score in enumerate(self.scores):
            if score[1] < new_score[1]:
                place = i
                break
        if place is not None:
            self.scores = self.scores[0:place] + [new_score] + self.scores[place:9]
            self.newest_score = place + 1
            return True
        else:
            self.newest_score = None
            return False


    def draw(self):

        # First prints the name of the
        title_text = g.MAIN_FONT.render(self.name, True, g.BLACK)
        title_text_rect = title_text.get_rect()
        title_text_rect.center = (g.WINDOW_WIDTH/2, g.MAIN_FONT.get_linesize())

        g.screen.blit(title_text, title_text_rect)


        linesize = g.SCORE_FONT.get_linesize()
        for i, score in enumerate(self.scores, 1):
            if i == self.newest_score:
                text_color = g.RED
            else:
                text_color = g.BLACK

            number_text = g.SCORE_FONT.render((str(i)+ '. '), True, text_color)
            number_text_rect = number_text.get_rect()
            number_text_rect.center = (g.WINDOW_WIDTH/5, (title_text_rect.bottom*2) + linesize*1.5*i)

            name_text = g.SCORE_FONT.render(score[0], True, text_color)
            name_text_rect = name_text.get_rect()
            name_text_rect.midleft = (number_text_rect.right, number_text_rect.centery)

            score_text = g.SCORE_FONT.render(str(score[1]), True, text_color)
            score_text_rect = score_text.get_rect()
            score_text_rect.center = (g.WINDOW_WIDTH*4/5, name_text_rect.centery)

            g.screen.blit(number_text, number_text_rect)
            g.screen.blit(name_text, name_text_rect)
            g.screen.blit(score_text, score_text_rect)

    def save(self):
        pickle_file = open(self.file_location, "wb")
        pickle.dump(self, pickle_file)
        pickle_file.close()

    @classmethod
    def load(cls):
        pickle_file = open(cls.file_location, "rb")
        return pickle.load(pickle_file)

    @classmethod
    def checkExist(cls):
        return os.path.isfile(cls.file_location)



