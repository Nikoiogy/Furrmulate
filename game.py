import sys
from collections import deque
from player import Player
from menu import Menu
from mapgeneration import generate_dungeon
from utils import GameState
from uihandler import UIHandler

class Game:
    def __init__(self, utils):
        self.utils = utils
        self.player = Player(self.utils)
        self.menu = Menu(self.utils)
        self.game_state = GameState.MAIN_MENU
        self.history = deque(maxlen=25)
        self.ui = UIHandler()
        self.ui.cleanup()

        self.dungeon = None
        self.command_handlers = {
            "test": self.handle_test,
            "exit": self.handle_exit,
            "save": self.handle_save,
            "map": self.handle_map,
            # "move": self.player.move,
            # "look": self.player.look,
            # "inventory": self.player.print_inventory,
            # "pickup": self.player.pickup,
            # "drop": self.player.drop,
            # "equip": self.player.equip,
            # "unequip": self.player.unequip,
            # "stats": self.player.print_stats,
            # "help": self.player.print_help,

            # Add more command handlers here
        }

    def start(self):
        while True:
            print(self.game_state.value)
            if self.game_state == GameState.MAIN_MENU:
                self.game_state = GameState(self.menu.main_menu())

            elif self.game_state == GameState.NEW:
                self.game_state = GameState(self.player.character_creation())

            elif self.game_state == GameState.LOAD:
                self.game_state = GameState(self.player.initialize_player())

            elif self.game_state == GameState.PLAYING:
                dungeon = generate_dungeon(10, 50)
                self.dungeon = dungeon
                self.game_loop()

            elif self.game_state == GameState.EXIT:
                sys.exit()

            else:
                self.game_state = GameState(self.menu.main_menu())

    def game_loop(self):
        self.utils.clear()
        alert = ""
        output = ""

        while self.game_state == GameState.PLAYING:
            self.utils.clear()

            self.ui.update_history(self.history)
            self.ui.update_output(output)
            command = self.ui.get_command()
            self.history.append(" # " + command)
            output = ""

            command = command.lower()

            handler = self.command_handlers.get(command)
            if handler:
                alert = ""
                try:
                    output = handler()
                except Exception as e:
                    alert = f"Error: {str(e)}"
            else:
                alert = "Invalid command!"
            
            self.ui.update_alert(alert)  # Update the alert message

        self.ui.cleanup()  # Clean up the UIHandler

    def handle_test(self):
        output = "Test command"
        return output

    def handle_exit(self):
        self.history.clear()
        self.game_state = GameState.MAIN_MENU

    def handle_save(self):
        pass

    def handle_map(self):
        self.ui.map_handler(self.dungeon)

    def handle_move(self):
        pass

    def handle_look(self):
        pass

    def handle_inventory(self):
        pass

    def handle_pickup(self):
        pass

    def handle_drop(self):
        pass

    def handle_equip(self):
        pass