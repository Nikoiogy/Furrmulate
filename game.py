import sys

from player import Player
from menu import Menu
from mapgeneration import generate_dungeon

from utils import Utils
utils = Utils()

class Game:
    def __init__(self):
        self.player = Player()
        self.game_state = "main_menu"

    def start(self):
        self.game_state = "main_menu"
        while True:
            print(self.game_state)
            if self.game_state == "main_menu":
                menu = Menu()
                self.game_state = menu.main_menu()

            elif self.game_state == "new":
                self.game_state = self.player.character_creation()

            elif self.game_state == "load":
                self.game_state = self.player.initialize_player()

            elif self.game_state == "playing":
                dungeon, spawn = generate_dungeon(10, 50)
                self.player.x, self.player.y = spawn
                self.game_loop(dungeon, spawn)

            elif self.game_state == "exit":
                sys.exit()

            else:
                self.game_state = menu.main_menu()

    def game_loop(self, dungeon, spawn):
        Utils.clear()
        alert = ""

        history = []
        while self.game_state == "playing":
            if len(history) > 50:
                history.pop(0)

            Utils.clear()

            print(history[-5:])

            command = input(utils.color_text("Enter a command ", "yellow") + alert + "# ")
            history.append(command)

            command = command.lower()

            if command == "exit":
                self.game_state = "main_menu"
                break
            elif command == "save":
                pass
            elif command == "help":
                pass
            elif command in ["history", "hist", "h", "log", "l"]:
                for line in history:
                    print(line)

            elif command == "inventory":
                pass
            elif command == "stats":
                pass
        
            elif command == "look":
                pass
            
            ########## Seperater ##########
            elif command in ["north", "n", "up", "w"]:
                if dungeon[self.player.y - 1][self.player.x].passable:
                    self.player.y -= 1
                else:
                    alert = utils.color_text("\nYou can't go that way! ", "red")
            ########## Seperater ##########
            elif command in ["south", "s", "down"]:
                if dungeon[self.player.y + 1][self.player.x].passable:
                    self.player.y += 1
                else:
                    alert = utils.color_text("\nYou can't go that way! ", "red")
            ########## Seperater ##########
            elif command in ["east", "e", "right", "d"]:
                if dungeon[self.player.y][self.player.x + 1].passable:
                    self.player.x += 1
                else:
                    alert = utils.color_text("\nYou can't go that way! ", "red")
            ########## Seperater ##########
            elif command in ["west", "w", "left", "a"]:
                if dungeon[self.player.y][self.player.x - 1].passable:
                    self.player.x -= 1
                else:
                    alert = utils.color_text("\nYou can't go that way! ", "red")

            else:
                alert = utils.color_text("\nInvalid command! ", "red")