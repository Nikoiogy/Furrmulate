import sys
import random
import pickle
from collections import deque
from tqdm import tqdm
from player import Player
from menu import Menu
from mapgeneration import generate_world
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

        self.command_handlers = {
            "test": self.handle_test,
            "exit": self.handle_exit,
            "save": self.handle_save,
            "move": self.handle_move,
            # "look": self.player.look,
            # "inventory": self.player.print_inventory,
            # "pickup": self.player.pickup,
            # "drop": self.player.drop,
            # "equip": self.player.equip,
            # "unequip": self.player.unequip,
            # "stats": self.player.print_stats,
            # "help": self.player.print_help,

            # DEBUG COMMANDS
            "saveworld": self.save_world,
        }

    def loading_screen(self, message, input_function):
        self.utils.clear()
        print(message)
        
        # Create a progress bar
        with tqdm(total=100) as pbar:
            previous_progress = 0
            result = None
            for progress, output in input_function():
                # Update the progress bar with the increment
                pbar.update(progress - previous_progress)
                previous_progress = progress
                result = output

        print("Loading complete!")
        return result

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
                if self.utils.debug_mode:
                    debug_world_filepath = "data/maps/debug-world.pkl"

                    with open(debug_world_filepath, "rb") as file:
                        self.world = pickle.load(file)
                else:
                    self.world = self.loading_screen("Generating world...", lambda: generate_world(400))

                self.spawn = random.choice([cell for row in self.world for cell in row if cell.passable])
                self.player.set_position(self.spawn.x, self.spawn.y)
                self.game_loop()

            elif self.game_state == GameState.EXIT:
                sys.exit()

            else:
                self.game_state = GameState(self.menu.main_menu())

    def game_loop(self):
        self.utils.clear()
        alert = ""
        output = ""
        self.ui.map_handler(self.world, self.player.x, self.player.y)

        while self.game_state == GameState.PLAYING:
            self.utils.clear()
            
            # Update the UI
            self.ui.update_history(self.history)
            self.ui.update_output(output)

            # Get the player's command
            command = self.ui.get_command()
            self.history.append(" # " + command)
            output = ""

            # Split the command into words for argument parsing
            command = command.lower().split()

            # Check if the command is not empty
            if command:
                handler = self.command_handlers.get(command[0])
                if handler:
                    alert = ""
                    try:
                        output = handler(*command[1:])  # Pass any additional words as arguments
                    except Exception as e:
                        alert = f"Error: {e}"
                else:
                    alert = "Invalid command!"
            else:
                alert = "Empty command!"
            
            self.ui.update_alert(alert)

        self.ui.cleanup()

    ## COMMAND HANDLERS ##
    def handle_test(self):
        output = "Test command"
        return output

    def handle_exit(self):
        self.history.clear()
        self.game_state = GameState.MAIN_MENU

    def handle_save(self):
        pass

    # PLAYER COMMANDS
    def handle_move(self, direction):
        output = self.player.move(direction, self.world)
        self.ui.map_handler(self.world, self.player.x, self.player.y) 
        return output

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

    # DEBUG COMMANDS

    def save_world(self):
        with open("data/maps/debug-world.pkl", "wb") as file:
            pickle.dump(self.world, file)
        return "World saved!"