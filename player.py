import os
import json
import re
from utils import GameState

class Player:
    def __init__(self, utils):
        self.utils = utils
        self.name = ""
        self.class_name = ""
        self.attributes = {
            "Strength": 0,
            "Intelligence": 0,
            "Willpower": 0,
            "Agility": 0,
            "Endurance": 0,
            "Charisma": 0,
            "Luck": 0
        }
        self.attribute_points = 18
        self.level = 1
        self.experience = 0
        self.petos = 0 # Currency
        self.inventory = []
        self.quests = []

        self.x = 0
        self.y = 0

    def character_creation(self):
        alert = ""
        self.utils.clear()

        def point_distribution():
            nonlocal alert

            def print_attribute_description(attribute_name):
                descriptions = {
                    "Strength": "Affects your character's physical strength and damage.",
                    "Intelligence": "Affects your character's magical strength and damage.",
                    "Willpower": "Affects your character's resistance to magic.",
                    "Agility": "Affects your character's speed and ability to dodge attacks.",
                    "Endurance": "Affects your character's health and resistance to physical attacks.",
                    "Charisma": "Affects your character's ability to persuade others.",
                    "Luck": "Affects your character's chance of getting a critical hit."
                }
                print("\n" + descriptions[attribute_name])

            temp_attributes = self.attributes.copy()
            temp_attribute_points = self.attribute_points

            while True:
                self.utils.clear()
                print("Point Distribution\n")
                print("You have", temp_attribute_points, "points remaining.")
                print("1) Strength:", temp_attributes["Strength"])
                print("2) Intelligence:", temp_attributes["Intelligence"])
                print("3) Willpower:", temp_attributes["Willpower"])
                print("4) Agility:", temp_attributes["Agility"])
                print("5) Endurance:", temp_attributes["Endurance"])
                print("6) Charisma:", temp_attributes["Charisma"])
                print("7) Luck:", temp_attributes["Luck"])
                print("\n0) Done")
                print("9) Cancel")

                option = input(self.utils.color_text("Choose an attribute to change or an option ", "yellow") + alert + "# ")

                if option == "0":
                    alert = ""
                    self.attributes = temp_attributes
                    self.attribute_points = temp_attribute_points
                    break
                elif option == "9":
                    alert = ""
                    return
                elif option in ["1", "2", "3", "4", "5", "6", "7"]:
                    attribute_name = list(temp_attributes.keys())[int(option) - 1]
                    try:
                        alert = ""
                        print_attribute_description(attribute_name)
                        value = int(input(self.utils.color_text("Enter the new value for " + attribute_name + " ", "yellow") + alert + "# "))
                        if value < 0 or value > temp_attribute_points + temp_attributes[attribute_name]:
                            alert = self.utils.color_text("\nInvalid input. Please enter a valid number between 0 and " + str(
                                temp_attribute_points + temp_attributes[attribute_name]) + ". ", "red")
                        else:
                            temp_attribute_points += temp_attributes[attribute_name] - value
                            temp_attributes[attribute_name] = value
                            alert = ""
                    except ValueError:
                        alert = self.utils.color_text("\nInvalid input. Please enter a valid number. ", "red")
                else:
                    alert = self.utils.color_text("\nInvalid input. Please try again. ", "red")

        def choose_class():
            nonlocal alert

            def print_class_description(class_name):
                descriptions = {
                    "Warrior": "A strong and skilled fighter who excels in close combat.",
                    "Mage": "A master of magic who can cast powerful spells.",
                    "Rogue": "A stealthy and agile character who specializes in sneak attacks."
                }
                print("\n" + descriptions[class_name])

            while True:
                self.utils.clear()
                print("Character Creation\n")
                print("1) Warrior")
                print("2) Mage")
                print("3) Rogue")
                print("\n9) Cancel")
                class_option = input(self.utils.color_text("Choose a class or an option ", "yellow") + alert + "# ")
                if class_option == "9":
                    return ""
                elif class_option == "1":
                    self.class_name = "Warrior"
                elif class_option == "2":
                    self.class_name = "Mage"
                elif class_option == "3":
                    self.class_name = "Rogue"
                else:
                    alert = self.utils.color_text("\nInvalid input. Please try again. ", "red")
                    continue
                print_class_description(self.class_name)
                class_confirmation = input("Choose this class? \n0) Yes \n9) No \n# ")
                if class_confirmation == "0":
                    return self.class_name
                elif class_confirmation == "9":
                    continue
                else:
                    alert = self.utils.color_text("\nInvalid input. Please try again. ", "red")
                    continue

        while True:
            self.utils.clear()
            print("Character Creation\n")

            print("1) Choose Name")
            print("2) Choose Class")
            print("3) Point Distribution")
            print("\n0) Done")
            print("9) Cancel")

            option = input(self.utils.color_text("Select an option ", "yellow") + alert + "# ")

            if option == "0":
                if self.class_name == "":
                    alert = self.utils.color_text("\nPlease choose a name. ", "red")
                    continue
                elif self.class_name == "":
                    alert = self.utils.color_text("\nPlease choose a class. ", "red")
                    continue
                elif self.attribute_points > 0:
                    alert = self.utils.color_text("\nPlease distribute all attribute points. ", "red")
                    continue
                else:
                    character = {
                        "name": self.name,
                        "class": self.class_name,
                        "attributes": self.attributes
                    }

                    # Show summary of character
                    self.utils.clear()
                    print("Character Summary\n")
                    print("Name:", self.name)
                    print("Class:", self.class_name)
                    print("\nAttributes:")
                    for attribute in self.attributes:
                        print(attribute + ":", self.attributes[attribute])
                    print("\n0) Confirm")
                    print("9) Back")
                    option = input(self.utils.color_text("Select an option ", "yellow") + alert + "# ")

                    if option == "0":

                        # Create the chars directory if it doesn't exist
                        if not os.path.exists("chars"):
                            os.makedirs("chars")

                        if os.path.exists(f"chars/{self.name}-starter.json"):
                            option = input(self.utils.color_text("\nA character with this name already exists. Do you want to overwrite it? ", "red") + alert + "\n0) Yes\n9) No\n# ")
                            if option == "0":
                                file_path = f"chars/{self.name}-starter.json"
                                with open(file_path, "w") as file:
                                    json.dump(character, file)
                                return GameState.PLAYING ### START GAME

                            elif option == "9":
                                alert = ""
                                continue
                            else:
                                alert = self.utils.color_text("\nInvalid input. Please try again. ", "red")
                                continue
                        else:
                            file_path = f"chars/{self.name}.json"
                            with open(file_path, "w") as file:
                                json.dump(character, file)

                            return "playing" ### START GAME

                    elif option == "9":
                        alert = ""
                        continue

            elif option == "1":
                alert = ""

                while True:
                    self.utils.clear()
                    print("Character Creation\n")
                    name = input(self.utils.color_text("Enter your character's name ", "yellow") + alert + "\n# ")

                    # Check if name is empty, is more than three characters, and doesn't start or end with a space, apostrophe, and/or period
                    if not re.match(r"^[a-zA-Z'.\s]{3,}$", name.strip()) or name.startswith(" ") or name.endswith(" ") or name.startswith("'") or name.endswith("'") or name.startswith(".") or name.endswith("."):
                        alert = self.utils.color_text(
                            "\nInvalid input. Please enter a valid name. Name must have at least 3 letters and can include letters, apostrophes, periods, and spaces. Name cannot begin or end with a space. ",
                            "red")
                        continue
                    else:
                        self.name = name
                        break

                alert = ""

            elif option == "2":
                alert = ""
                self.class_name = choose_class()

            elif option == "3":
                alert = ""
                point_distribution()

            elif option == "9":
                option = input(self.utils.color_text("\nAre you sure you want to cancel? ", "red") + alert + "\n0) Yes\n9) No\n# ")
                if option == "0":
                    return GameState.MAIN_MENU ### EXIT TO MAIN MENU

                elif option == "9":
                    alert = ""
                    continue

            else:
                alert = self.utils.color_text("\nInvalid input. Please try again. ", "red")

    def initialize_player(self):
        alert = ""

        # Get list of characters
        characters = []
        for file in os.listdir("chars"):
            if file.endswith(".json"):
                characters.append(file.split(".")[0])

        # If there are no characters, return to main menu
        if len(characters) == 0:
            print("No characters found.")
            input(self.utils.color_text("\nPress enter to continue # ", "yellow"))
            return GameState.MAIN_MENU ### EXIT TO MAIN MENU

        while True:
            # Select character
            while True:
                self.utils.clear()
                print("Select Character\n")

                for i in range(len(characters)):
                    print(str(i + 1) + ") " + characters[i])

                print("\n0) Back")

                option = input(self.utils.color_text("Select a character ", "yellow") + alert + "# ")
                if option == "0":
                    return GameState.MAIN_MENU ### EXIT TO MAIN MENU
                elif option in [str(i + 1) for i in range(len(characters))]:
                    file_path = f"chars/{characters[int(option) - 1]}.json"
                    with open(file_path, "r") as file:
                        character = json.load(file)
                    self.name = character["name"]
                    self.class_name = character["class"]
                    self.attributes = character["attributes"]
                    break
                else:
                    alert = self.utils.color_text("\nInvalid input. Please try again. ", "red")

            while True:
                self.utils.clear()
                print("Character Summary\n")
                print("Name:", self.name)
                print("Class:", self.class_name)
                print("\nAttributes:")
                for attribute in self.attributes:
                    print(attribute + ":", self.attributes[attribute])
                print("\n0) Confirm")
                print("9) Back")
                option = input(self.utils.color_text("Select an option ", "yellow") + alert + "# ")

                if option == "0":
                    return GameState.PLAYING ### START GAME
                elif option == "9":
                    alert = ""
                    break
                else:
                    alert = self.utils.color_text("\nInvalid input. Please try again. ", "red")
                    continue

    # Commands
