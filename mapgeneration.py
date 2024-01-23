import random

# Cell Classes

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visible = False

class Wood_Wall(Cell):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.symbol = "▓"
        self.color = "brown"
        self.name = "Wood Wall"
        self.passable = False

class Stone_Wall(Cell):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.symbol = "▓"
        self.color = "gray"
        self.name = "Stone Wall"
        self.passable = False

class Dirt_Floor(Cell):
    def __init__(self, x, y, wet, npc):
        super().__init__(x, y)
        self.symbol = "░"
        self.color = "brown"
        self.name = "Dirt Floor"
        self.passable = True
        self.wet = wet
        # self.npc = npc Implement later

class Stone_Floor(Cell):
    def __init__(self, x, y, wet, npc):
        super().__init__(x, y)
        self.symbol = "░"
        self.color = "gray"
        self.name = "Stone Floor"
        self.passable = True
        self.wet = wet
        # self.npc = npc Implement later

class Water(Cell):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.symbol = "░"
        self.color = "blue"
        self.name = "Water"
        self.passable = False

class Door(Cell):
    def __init__(self, x, y,):
        super().__init__(x, y)
        self.symbol = "░"
        self.color = "brown"
        self.name = "Door"
        self.passable = True
        self.open = False

class Chest(Cell):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.symbol = "░"
        self.color = "brown"
        self.name = "Chest"
        self.passable = True
        self.open = False

class Trap(Cell):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.symbol = "░"
        self.color = "brown"
        self.name = "Trap"
        self.passable = True
        self.visible = False

# def generate_dungeon()