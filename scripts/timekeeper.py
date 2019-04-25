# This module conatins the GameTime Class which is used to create an object that tracks the time of day and day of the week inside of the game

class GameTime:
    day = 0
    time = 0
    days_of_week = ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')
    times_of_day = ('Morning', 'Afternoon', 'Evening', 'Night')
    max_day = len(days_of_week)

    def incrementTime(self):
        self.time += 1
        if self.time == len(self.times_of_day):
            self.incrementDay()

    def incrementDay(self):
        self.day += 1  # increases the day of the week
        self.time = 0  # sets time to morning

    def timeOver(self):
        if self.day == self.max_day:
            return True
        else:
            return False
