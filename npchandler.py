# Used to generzte NPCs for the game

import random

# Importing data from a file

with open('data/names.txt', 'r') as file:
    names = file.read().split(',')

# NPC Classes

class NPCStats_Generator:
    def __init__(self, player_level, difficulty, isenemy):
        self.player_level = player_level
        self.difficulty = difficulty
        self.isenemy = isenemy
        self.stats = self.generate_stats()

    def generate_stats(self):
        npc_class = self.generate_class()

        stats = {
            "health": self.generate_health(self.player_level, self.difficulty, npc_class, self.isenemy),
            "class": npc_class,
            "attributes": self.generate_attributes(npc_class, self.player_level),
        }

        return stats

    def generate_class(self):
        classes = ["warrior", "mage", "rogue"]
        return random.choice(classes)

    def generate_attributes(self, npc_class, player_level):
        attributes = {
            "strength": 0,
            "intelligence": 0,
            'willpower': 0,
            'agility': 0,
            'endurance': 0,
            'luck': 0
        }

        points = 15 + (player_level * 4)

        major_atr_max = points // 4
        major_atr_min = points // 6

        if npc_class == "warrior":
            attributes["strength"] = random.randint(major_atr_min, major_atr_max)
            attributes["endurance"] = random.randint(major_atr_min, major_atr_max)
            attributes["agility"] = random.randint(major_atr_min, major_atr_max)
            points -= attributes["strength"] + attributes["endurance"] + attributes["agility"]
        elif npc_class == "mage":
            attributes["intelligence"] = random.randint(major_atr_min, major_atr_max)
            attributes["willpower"] = random.randint(major_atr_min, major_atr_max)
            attributes["endurance"] = random.randint(major_atr_min, major_atr_max)
            points -= attributes["intelligence"] + attributes["willpower"] + attributes["endurance"]
        elif npc_class == "rogue":
            attributes["agility"] = random.randint(major_atr_min, major_atr_max)
            attributes["luck"] = random.randint(major_atr_min, major_atr_max)
            attributes["endurance"] = random.randint(major_atr_min, major_atr_max)
            points -= attributes["agility"] + attributes["luck"] + attributes["endurance"]

        while points > 0:
            attribute = random.choice(list(attributes.keys()))
            attributes[attribute] += 1
            points -= 1

        return attributes


    def generate_health(self, player_level, difficulty, npc_class, isenemy):
        if isenemy:
            if npc_class == "warrior":
                health = (random.randint(15, 25) + (player_level * 2)) * (difficulty * 0.15)
            elif npc_class == "mage":
                health = (random.randint(15, 20) + (player_level * 2)) * (difficulty * 0.15)
            elif npc_class == "rogue":
                health = (random.randint(15, 20) + (player_level * 2)) * (difficulty * 0.15)
        else:
            health = -1

        return round(health)
    
class NPC:
    def __init__(self, player_level, difficulty, isenemy):
        self.name = random.choice(names)
        self.stats = NPCStats_Generator(player_level, difficulty, isenemy).stats
    
    def __str__(self):
        return f"NPC Name: {self.name} the {self.stats['class'].capitalize()}, Stats: {self.stats}"

print(NPC(25, 5, True))