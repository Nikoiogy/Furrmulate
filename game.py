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
        while self.game_state == "playing":
            command = input(utils.color_text("Enter a command ", "yellow") + alert + "# ")