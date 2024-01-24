import random

# from npchandler import NPC
from utils import color_text

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

def generate_dungeon(num_rooms, size):
    dungeon = [[Stone_Wall(x, y) for x in range(size)] for y in range(size)]

    rooms = []

    for i in range(num_rooms):
        room_size = random.randint(5, 8)
        room_x = random.randint(1, size - room_size - 2)
        room_y = random.randint(1, size - room_size - 2)
        
        timeout = 0

        # Check if there are any existing dirt floors in the potential room area
        while any(isinstance(dungeon[y][x], Dirt_Floor) for y in range(room_y - 1, room_y + room_size + 1) for x in range(room_x - 1, room_x + room_size + 1)):
            # Generate new random coordinates for the room
            room_x = random.randint(1, size - room_size - 2)  
            room_y = random.randint(1, size - room_size - 2)

            timeout += 1

            # If the timeout limit is reached, exit the loop
            if timeout > size * size:
                print("Timeout")
                break

        else:
            # Create dirt floors for the room
            for y in range(room_y, room_y + room_size):
                for x in range(room_x, room_x + room_size):
                    dungeon[y][x] = Dirt_Floor(x, y, False, None)

            # Add walls surrounding the room
            for y in range(room_y - 1, room_y + room_size + 1):
                for x in range(room_x - 1, room_x + room_size + 1):
                    if not isinstance(dungeon[y][x], Dirt_Floor):
                        dungeon[y][x] = Wood_Wall(x, y)
            
            rooms.append((room_x, room_y, room_size))

    # Create corridors between rooms
    for i in range(len(rooms) - 1):
        room_x, room_y, room_size = rooms[i]
        next_room_x, next_room_y, next_room_size = rooms[i + 1]

        # Calculate the start and end points of the corridor
        start_x = room_x + room_size // 2
        start_y = room_y + room_size // 2
        end_x = next_room_x + next_room_size // 2
        end_y = next_room_y + next_room_size // 2

        # Create the corridor
        x, y = start_x, start_y
        while x != end_x or y != end_y:
            if x != end_x:
                x += 1 if end_x > x else -1
            elif y != end_y:
                y += 1 if end_y > y else -1

            # Check if the cell is not a part of another room
            if not isinstance(dungeon[y][x], Dirt_Floor):
                dungeon[y][x] = Dirt_Floor(x, y, False, None)

                # Add walls around the corridor
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < size and 0 <= ny < size and not isinstance(dungeon[ny][nx], Dirt_Floor):
                        dungeon[ny][nx] = Wood_Wall(nx, ny)

    return dungeon


def print_dungeon(dungeon):
    for row in dungeon:
        for cell in row:
            if isinstance(cell, Dirt_Floor):
                print(color_text("D","brown"), end=" ")
            elif isinstance(cell, Wood_Wall):
                print("W", end=" ")
            else:
                print("_", end=" ")
        print()

print_dungeon(generate_dungeon(10, 60))