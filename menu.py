from utils import GameState
from player import Player

class Menu:
    def __init__(self, utils):
        self.utils = utils
        self.alert = ""

    def main_menu(self):
        while True:
            self.utils.clear()
            print("Welcome to the Text RPG!\n")
            print("1) New Character")
            print("2) Load Character")
            print("3) Settings")
            print("\n9) Exit")
            option = input(self.utils.color_text("Select an option ", "yellow") + self.alert + "# ")
            if option == "9":
                return GameState.EXIT
                
            elif option == "1":
                self.alert = ""
                return GameState.NEW
                    
            elif option == "2":
                self.alert = ""
                return GameState.LOAD
                
            elif option == "3":
                self.alert = ""
                self.settings()

            else:
                self.alert = self.utils.color_text("\nInvalid input. Please try again. ", "red")

    def settings(self):
        while True:
            self.utils.clear()
            print("Settings\n")
            print("Game Settings")
            print("1) Change Name")
            print("2) Change Difficulty")
            print("\nAccessibility Settings")
            print("3) Color Mode: " + (self.utils.color_text("On", "green") if self.utils.color_mode else "Off"))
            print("4) Text Speed: " + self.utils.text_speed)
            print("\Development Settings")
            print("5) Debug Mode: " + (self.utils.color_text("On", "green") if self.utils.debug_mode else "Off"))
            print("\n9) Back")
            option = input(self.utils.color_text("Select an option ", "yellow") + self.alert + "# ")
            if option == "9":
                self.alert = ""
                return GameState.MAIN_MENU
            elif option == "1":
                self.alert = self.utils.color_text("\nNot yet available! ", "red")
            elif option == "2":
                self.alert = self.utils.color_text("\nNot yet available! ", "red")
            elif option == "3":
                self.utils.color_mode = not self.utils.color_mode
                self.alert = ""
            elif option == "4":
                self.alert = self.utils.color_text("\nNot yet available! ", "red")
            elif option == "5":
                self.utils.debug_mode = not self.utils.debug_mode
                self.alert = ""
            else:
                self.alert = self.utils.color_text("\nInvalid input. Please try again. ", "red")