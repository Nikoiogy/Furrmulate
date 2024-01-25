import sys
from collections import deque
from player import Player
from menu import Menu
from mapgeneration import generate_dungeon
from utils import Utils, GameState
from uihandler import UIHandler

utils = Utils()

class Game:
    def __init__(self):
        self.player = Player()
        self.game_state = GameState.MAIN_MENU
        self.history = deque(maxlen=5)
        self.command_handlers = {
            "test": self.handle_test,
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

        ui = UIHandler()  # Initialize the UIHandler outside the game loop

        while self.game_state == GameState.PLAYING:
            Utils.clear()

            ui.update_history(self.history)
            ui.update_output(output)
            command = ui.get_command()
            self.history.append(command)
            output = ""

            command = command.lower()

            handler = self.command_handlers.get(command)
            if handler:
                alert = ""
                output = handler()
            else:
                alert = "Invalid command!"
            
            ui.update_alert(alert)  # Update the alert message

        ui.cleanup()  # Clean up the UIHandler`

    def handle_test(self):
        output = "Test command"
        return output

    def handle_exit(self):
        self.history.clear()
        self.game_state = GameState.MAIN_MENU

    def handle_save(self):
        pass

    # Add more command handler methods here