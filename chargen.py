# Character Generator - PyGame Edition
# This module handles the stats that both the character and enemies have and the functions that they have'

import random


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
            print("%s dodges %s's attack" % (opponent.name, self.name))
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

            # Finally damage is dealt and printed to the screen
            opponent.current_health -= damage
            print("%s deals %d damage to %s" % (self.name, damage, opponent.name))
            # Checks if opponent is still alive
            opponent.check_alive()

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

    def display_stats(self):
        print("%s \nHealth: %d/%d" % (self.name, self.current_health, self.max_health))
        print()


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

    def sleep(self):
        self.current_health = self.max_health
        print("You sleep and fully heal yourself")
        print()

    def display_full_stats(self):
        print("%s \nHealth: %d/%d" % (self.name, self.current_health, self.max_health))
        print("Strength: %d \tAgility: %d \tAccuracy: %d" % (self.strength, self.agility, self.accuracy))
        print("Gold : %d \tEnemies Killed: %d" % (self.gold, self.enemies_killed))
        print()

    def collect_gold(self, opponent):
        self.gold += opponent.gold
        self.total_gold += opponent.gold
        print("%s collected %d gold from %s" % (self.name, opponent.gold, opponent.name))
        print()
