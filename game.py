from player import Player
from menu import Menu

from utils import Utils, alert

class Game:
    def __init__(self):
        self.player = Player()
        self.game_state = "main_menu"

    def start(self):
        self.game_state = "main_menu"
        while True:
            if self.game_state == "main_menu":
                menu = Menu()
                self.game_state = menu.main_menu()

            elif self.game_state == "load":
                self.game_state = self.player.initialize_player()

            elif self.game_state == "playing":
                self.game_loop()

            elif self.game_state == "exit":
                break
            else:
                self.game_state = menu.main_menu()

    def game_loop(self):
        player = self.player
        print(player.name)
