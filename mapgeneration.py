import random
import pickle

from perlin_noise import PerlinNoise
# from npchandler import NPC
from utils import Utils

utils = Utils()

# Cell Classes

class Cell:
    def __init__(self, x, y, symbol, color, name, passable):
        self.x = x
        self.y = y
        self.visible = False
        self.symbol = symbol
        self.color = color
        self.name = name
        self.passable = passable

# FORMAT: class_name = Cell(x, y, symbol, color, name, passable)
def create_cell(x, y, type):
    cell_dict = {
        "grass_floor": Cell(x, y, "G", "green", "Grass Floor", True),
        "sand_floor": Cell(x, y, "S", "yellow", "Sand Floor", True),
        "dirt_floor": Cell(x, y, "D", "brown", "Dirt Floor", True),
        "stone_floor": Cell(x, y, "F", "gray", "Stone Floor", True),
        "water": Cell(x, y, "W", "blue", "Water", False),
        "door": Cell(x, y, "O", "brown", "Door", True),
        "chest": Cell(x, y, "C", "brown", "Chest", True),
        "trap": Cell(x, y, "T", "brown", "Trap", True),
        "tree_trunk": Cell(x, y, "T", "brown", "Tree Trunk", False),
        "wood_wall": Cell(x, y, "W", "brown", "Wood Wall", False),
        "stone_wall": Cell(x, y, "W", "gray", "Stone Wall", False),
        "empty": Cell(x, y, "E", "black", "Empty", False),
        "dungeon_entrance": Cell(x, y, "E", "black", "Dungeon Entrance", True)
    }
    return cell_dict[type]

def generate_world(size):
    world = [[create_cell(x, y, "grass_floor") for x in range(size)] for y in range(size)]

    # Add lakes using Perlin noise
    noise = PerlinNoise(octaves=6, seed=random.randint(0, 1000))
    total_cells = size * size
    total_trees = 100
    total_work = total_cells + total_trees  # Include trees in total work
    work_done = 0

    for y in range(size):
        for x in range(size):
            noise_value = noise([x / size, y / size])
            noise_value = (noise_value + 1) / 2  # Normalize to [0, 1]
            if noise_value < 0.4:  # Adjust the threshold value here
                world[y][x] = create_cell(x, y, "water")
            if noise_value > 0.4 and noise_value < 0.42:
                world[y][x] = create_cell(x, y, "sand_floor")

            work_done += 1
            progress = round(work_done / total_work * 100)  # Calculate progress as a percentage
            yield progress, world  # Yield progress and world

    # Add trees
    for i in range(total_trees):
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        if world[y][x].name == "Grass Floor":
            world[y][x] = create_cell(x, y, "tree_trunk")

        work_done += 1
        progress = round(work_done / total_work * 100)  # Update progress after each tree
        yield progress, world  # Yield progress and world

    return world

def generate_dungeon(num_rooms, size):
    dungeon = [[create_cell(x, y, "empty") for x in range(size)] for y in range(size)]

    rooms = []

    # Create rooms
    for i in range(num_rooms):
        room_size = random.randint(5, 8)
        room_x = random.randint(1, size - room_size - 2)
        room_y = random.randint(1, size - room_size - 2)
        
        timeout = 0

        # Check if there are any existing dirt floors in the potential room area
        while any(isinstance(dungeon[y][x], Cell) for y in range(room_y - 1, room_y + room_size + 1) for x in range(room_x - 1, room_x + room_size + 1)):
            # Generate new random coordinates for the room
            room_x = random.randint(1, size - room_size - 2)  
            room_y = random.randint(1, size - room_size - 2)

            timeout += 1

            # If the timeout limit is reached, exit the loop
            if timeout > size * size:
                print("Timeout")
                break

        else:
            # Create cells for the room
            for y in range(room_y, room_y + room_size):
                for x in range(room_x, room_x + room_size):
                    dungeon[y][x] = create_cell(x, y, "dirt_floor")

            # Add walls surrounding the room
            for y in range(room_y - 1, room_y + room_size + 1):
                for x in range(room_x - 1, room_x + room_size + 1):
                    if not isinstance(dungeon[y][x], Cell):
                        dungeon[y][x] = create_cell(x, y, "wood_wall")
            
            rooms.append((room_x, room_y, room_size))

    # Create corridors between rooms
    for i in range(len(rooms) - 1):
        room_x, room_y, room_size = rooms[i]
        next_room_x, next_room_y, next_room_size = rooms[i + 1]

        # Calculate the start and end points of the corridor
        start_x = random.choice([room_x, room_x + room_size - 1])
        start_y = random.choice([room_y, room_y + room_size - 1])
        end_x = random.choice([next_room_x, next_room_x + next_room_size - 1])
        end_y = random.choice([next_room_y, next_room_y + next_room_size - 1])

        # Create the corridor
        x, y = start_x, start_y
        while x != end_x or y != end_y:
            if x != end_x:
                x += 1 if end_x > x else -1
            elif y != end_y:
                y += 1 if end_y > y else -1

            # Check if the cell is not a part of another room
            if not isinstance(dungeon[y][x], Cell):
                dungeon[y][x] = create_cell(x, y, "dirt_floor")

                # Add walls around the corridor
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < size and 0 <= ny < size and not isinstance(dungeon[ny][nx], Cell):
                        dungeon[ny][nx] = create_cell(nx, ny, "wood_wall")
    
    return dungeon

def print_map(world):
    for row in world:
        for cell in row:
            print(utils.color_text(cell.symbol, cell.color), end=" ")
        print()