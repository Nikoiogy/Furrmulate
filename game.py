import sys
from collections import deque
from player import Player
from menu import Menu
from mapgeneration import generate_dungeon

from utils import Utils, GameState
utils = Utils()

class Game:
    def __init__(self):
        self.player = Player()
        self.game_state = GameState.MAIN_MENU
        self.history = deque(maxlen=5)
        self.command_handlers = {
            "exit": self.handle_exit,
            "save": self.handle_save,
            # Add more command handlers here
        }

    def start(self):
        while True:
            print(self.game_state.value)
            if self.game_state == GameState.MAIN_MENU:
                menu = Menu()
                self.game_state = GameState(menu.main_menu())

            elif self.game_state == GameState.NEW:
                self.game_state = GameState(self.player.character_creation())

            elif self.game_state == GameState.LOAD:
                self.game_state = GameState(self.player.initialize_player())

            elif self.game_state == GameState.PLAYING:
                dungeon, spawn = generate_dungeon(10, 50)
                self.player.x, self.player.y = spawn
                self.game_loop(dungeon)

            elif self.game_state == GameState.EXIT:
                sys.exit()

            else:
                self.game_state = GameState(menu.main_menu())

    def game_loop(self, dungeon):
        Utils.clear()
        alert = ""
        output = ""

        while self.game_state == GameState.PLAYING:
            Utils.clear()

            print("\n # ".join(self.history))

            print(output)
            command = input(utils.color_text("Enter a command ", "yellow") + alert + "# ")
            self.history.append(command)
            output = ""

            command = command.lower()

            handler = self.command_handlers.get(command)
            if handler:
                handler()
            else:
                alert = utils.color_text("\nInvalid command! ", "red")

    def handle_exit(self):
        self.game_state = GameState.MAIN_MENU

    def handle_save(self):
        pass

    # Add more command handler methods here