# Character Generator - PyGame Edition
# This module handles the stats that both the character and enemies have and the functions that they have
# Generates enemies by importing the csv from thew data folder

import random, csv
import scripts.my_globals as g


class Character:
    name = ""
    max_health = 0
    current_health = 0
    strength = 0
    agility = 0
    accuracy = 0
    alive = True

    def attack(self, opponent):

        dodge = opponent.attempt_dodge(self)
        if dodge:
            return 0
        else:
            # Damage is initialized to be equal to strength
            damage = self.strength

            # Rolls 1-5
            roll = random.randint(1, 5)
            # If accuracy beats or equals the roll, full damage is dealt
            # An accuracy of 1 is 20% chance to deal full damage, 2 is 40%, 3 is 60%, 4 is 80%, 5 is 100%

            # Otherwise the difference is subtracted from the damage dealt
            if self.accuracy < roll:
                damage -= (roll - self.accuracy)
                # if damage is 0 or less, 1 damage is dealt
                if damage <= 0:
                    damage = 1

            # Finally damage is dealt
            opponent.current_health -= damage
            # Checks if opponent is still alive
            opponent.check_alive()
            return damage

    def attempt_dodge(self, opponent):
        # If the opponent's accuracy is greater than or equal your agility, their attack always lands
        if opponent.accuracy >= self.agility:
            dodge = False
        # Else, an advantage is calculated based on the difference. If the roll is less than advantage the dodge is successful
        # Effectively, an advantage of 1 is a 20% chance, 2 is 40%, 3 is 60% and 4 is the maximum at 80%
        else:
            advantage = self.agility - opponent.accuracy
            roll = random.randint(0, 4)
            if roll < advantage:
                dodge = True
            else:
                dodge = False
        return dodge

    def check_alive(self):
        if self.current_health <= 0:
            self.alive = False
        else:
            self.alive = True


class Player(Character):
    def __init__(self, name):
        self.name = name
        self.max_health = 10
        self.current_health = self.max_health
        self.strength = 1
        self.agility = 1
        self.accuracy = 1
        self.gold = 0
        self.total_gold = 0
        self.enemies_killed = 0
        self.rare_killed = 0
        self.message = "You begin your hunt"

    def sleep(self):
        self.current_health = self.max_health

    def collect_gold(self, opponent):
        self.gold += opponent.gold
        self.total_gold += opponent.gold

    def killedEnemy(self, opponent):
        self.enemies_killed += 1
        if opponent.rare:
            self.rare_killed += 1
    
    def canTrain(self, skill):
    # skill is a string that identifies the skill that will be trained. Returns true or false
        skill_value = self.getSkillValue(skill)
        if skill_value < 5 and self.gold >= skill_value:
            return True
        else:
            return False
    
    def trainSkill(self, skill):
        # Increases the skill by one and reducing gold by the skill value        
        if skill == g.STR_STRENGTH:
            self.gold -= self.strength
            self.strength += 1
        if skill == g.STR_AGILITY:
            self.gold -= self.agility
            self.agility += 1
        if skill == g.STR_ACCURACY:
            self.gold -= self.accuracy
            self.accuracy += 1  
    
    def getSkillValue(self, skill):
        if skill == g.STR_STRENGTH:
            return self.strength
        if skill == g.STR_AGILITY:
            return self.agility
        if skill == g.STR_ACCURACY:
            return self.accuracy
        

class Enemy(Character):
    def __init__(self, data):
        # data is a dictionary pulled from the csv file
        self.name = data['name']
        self.max_health = int(data['health'])
        self.current_health = self.max_health
        self.strength = int(data['strength'])
        self.agility = int(data['agility'])
        self.accuracy = int(data['accuracy'])
        self.gold = int(data['gold'])
        self.rare = bool(data['rare'])

        # occurance rates
        self.morning_occ = int(data['morn_occ'])
        self.midday_occ = int(data['mid_occ'])
        self.evening_occ = int(data['eve_occ'])
        self.night_occ = int(data['night_occ'])


def getEnemyDataFrom(csv_file_name):
    # pulls dictionaries from each line of the csv file and returns a list of enemy objects

    enemy_list = []
    with open(csv_file_name) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            enemy = Enemy(row)
            enemy_list.append(enemy)
    return enemy_list


def getWeightedEnemyList(enemy_list, game_time):
    # takes a list of enemy objects and returns a weighted list of strings based on the time of day

    weighted_list = []
    if game_time.time == 0:  # time is morning
        for enemy in enemy_list:
            weighted_list += enemy.morning_occ*(enemy.name,)
    elif game_time.time == 1:  # time is mid-day
        for enemy in enemy_list:
            weighted_list += enemy.midday_occ*(enemy.name,)
    elif game_time.time == 2:  # time is evening
        for enemy in enemy_list:
            weighted_list += enemy.evening_occ*(enemy.name,)
    elif game_time.time == 3:
        for enemy in enemy_list:
            weighted_list += enemy.night_occ*(enemy.name,)

    return weighted_list


def generateEnemy(game_time):
    # calls functions to generate a weighted list of enemies and return a random choice from that list

    enemy_list = getEnemyDataFrom('data/enemies.csv')
    weighted_list = getWeightedEnemyList(enemy_list, game_time)

    # enemy_chosen is simply a string so enemy_list needs to searched for a matching name and that enemy object is returned
    enemy_chosen = random.choice(weighted_list)

    for enemy in enemy_list:
        if enemy_chosen == enemy.name:
            return enemy


