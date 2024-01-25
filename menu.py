from utils import Utils
utils = Utils()

from player import Player

class Menu:
    def __init__(self):
        self.alert = ""

    def main_menu(self):
        while True:  # Add this line
                Utils.clear()
                print("Welcome to the Text RPG!\n")
                print("1) New Character")
                print("2) Load Character")
                print("3) Settings")
                print("\n9) Exit")
                option = input(utils.color_text("Select an option ", "yellow") + self.alert + "# ")
                if option == "9":
                    return "exit"
                
                elif option == "1":
                    self.alert = ""
                    return "new"
                    
                elif option == "2":
                    self.alert = ""
                    return "load"
                
                elif option == "3":
                    self.alert = ""
                    self.settings()

                else:
                    self.alert = utils.color_text("\nInvalid input. Please try again. ", "red")

    def settings(self):
        Utils.clear()
        print("Settings\n")
        print("In-Game Settings")
        print("1) Change Name")
        print("2) Change Difficulty")
        print("\nAccessability Settings")
        print("3) Color Mode: " + (utils.color_text("On", "green") if utils.color_mode else "Off"))
        print("4) Text Speed: " + utils.text_speed)
        print("\n9) Back")
        option = input(utils.color_text("Select an option ", "yellow") + self.alert + "# ")
        if option == "9":
            self.alert = ""
            self.main_menu()
        elif option == "1":
            self.alert = utils.color_text("\nNot yet available! ", "red")
            self.settings()
        elif option == "2":
            self.alert = utils.color_text("\nNot yet available! ", "red")
            self.settings()
        elif option == "3":
            utils.color_mode = not utils.color_mode
            self.alert = ""
            self.settings()
        elif option == "4":
            self.alert = utils.color_text("\nNot yet available! ", "red")
            self.settings()
        else:
            self.alert = utils.color_text("\nInvalid input. Please try again. ", "red")
            self.settings()
