from utils import Utils, GameState
from player import Player

utils = Utils()

class Menu:
    def __init__(self):
        self.alert = ""

    def main_menu(self):
        while True:
            Utils.clear()
            print("Welcome to the Text RPG!\n")
            print("1) New Character")
            print("2) Load Character")
            print("3) Settings")
            print("\n9) Exit")
            option = input(utils.color_text("Select an option ", "yellow") + self.alert + "# ")
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
                self.alert = utils.color_text("\nInvalid input. Please try again. ", "red")

    def settings(self):
        while True:
            Utils.clear()
            print("Settings\n")
            print("In-Game Settings")
            print("1) Change Name")
            print("2) Change Difficulty")
            print("\nAccessibility Settings")
            print("3) Color Mode: " + (utils.color_text("On", "green") if utils.color_mode else "Off"))
            print("4) Text Speed: " + utils.text_speed)
            print("\n9) Back")
            option = input(utils.color_text("Select an option ", "yellow") + self.alert + "# ")
            if option == "9":
                self.alert = ""
                return GameState.MAIN_MENU
            elif option == "1":
                self.alert = utils.color_text("\nNot yet available! ", "red")
            elif option == "2":
                self.alert = utils.color_text("\nNot yet available! ", "red")
            elif option == "3":
                utils.color_mode = not utils.color_mode
                self.alert = ""
            elif option == "4":
                self.alert = utils.color_text("\nNot yet available! ", "red")
            else:
                self.alert = utils.color_text("\nInvalid input. Please try again. ", "red")