import os
import json
import re

from utils import clear, color_text, color_mode, text_speed, alert

# Character Creation Variables

character_name = ""
character_class = ""
attribute_points = 18
attributes = {
    "Strength": 0,
    "Intelligence": 0,
    "Willpower": 0,
    "Agility": 0,
    "Endurance": 0,
    "Charisma": 0,
    "Luck": 0
}

# Character Creation Functions

def point_distribution(attributes, attribute_points):
    global alert

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

    temp_attributes = attributes.copy()
    temp_attribute_points = attribute_points

    while True:
        clear()
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

        option = input(color_text("Choose an attribute to change or an option ", "yellow") + alert + "# ")

        if option == "0":
            alert = ""
            attributes = temp_attributes
            attribute_points = temp_attribute_points
            break
        elif option == "9":
            alert = ""
            return attributes, attribute_points
        elif option in ["1", "2", "3", "4", "5", "6", "7"]:
            attribute_name = list(temp_attributes.keys())[int(option) - 1]
            try:
                alert = ""
                print_attribute_description(attribute_name)
                value = int(input(color_text("Enter the new value for " + attribute_name + " ", "yellow") + alert + "# "))
                if value < 0 or value > temp_attribute_points + temp_attributes[attribute_name]:
                    alert = color_text("\nInvalid input. Please enter a valid number between 0 and " + str(
                        temp_attribute_points + temp_attributes[attribute_name]) + ". ", "red")
                else:
                    temp_attribute_points += temp_attributes[attribute_name] - value
                    temp_attributes[attribute_name] = value
                    alert = ""
            except ValueError:
                alert = color_text("\nInvalid input. Please enter a valid number. ", "red")
        else:
            alert = color_text("\nInvalid input. Please try again. ", "red")

    return attributes, attribute_points

def choose_class():
    global alert

    def print_class_description(class_name):
        descriptions = {
            "Warrior": "A strong and skilled fighter who excels in close combat.",
            "Mage": "A master of magic who can cast powerful spells.",
            "Rogue": "A stealthy and agile character who specializes in sneak attacks."
        }
        print("\n" + descriptions[class_name])

    while True:
        clear()
        print("Character Creation\n")
        print("1) Warrior")
        print("2) Mage")
        print("3) Rogue")
        print("\n9) Cancel")
        class_option = input(color_text("Choose a class or an option ", "yellow") + alert + "# ")
        if class_option == "9":
            return ""
        elif class_option == "1":
            character_class = "Warrior"
        elif class_option == "2":
            character_class = "Mage"
        elif class_option == "3":
            character_class = "Rogue"
        else:
            alert = color_text("\nInvalid input. Please try again. ", "red")
            continue
        print_class_description(character_class)
        class_confirmation = input("Choose this class? \n0) Yes \n9) No \n# ")
        if class_confirmation == "0":
            return character_class
        elif class_confirmation == "9":
            continue
        else:
            alert = color_text("\nInvalid input. Please try again. ", "red")
            continue

def character_creation():
    global alert
    global character_name
    global character_class
    global attributes
    global attribute_points

    clear()

    while True:
        clear()
        print("Character Creation\n")

        print("1) Choose Name")
        print("2) Choose Class")
        print("3) Point Distribution")
        print("\n0) Done")
        print("9) Cancel")

        option = input(color_text("Select an option ", "yellow") + alert + "# ")

        if option == "0":
            if character_class == "":
                alert = color_text("\nPlease choose a name. ", "red")
                continue
            elif character_class == "":
                alert = color_text("\nPlease choose a class. ", "red")
                continue
            elif attribute_points > 0:
                alert = color_text("\nPlease distribute all attribute points. ", "red")
                continue
            else:

                character = {
                    "name": character_name,
                    "class": character_class,
                    "attributes": attributes
                }

                # Show summary of character
                clear()
                print("Character Summary\n")
                print("Name:", character_name)
                print("Class:", character_class)
                print("\nAttributes:")
                for attribute in attributes:
                    print(attribute + ":", attributes[attribute])
                print("\n0) Confirm")
                print("9) Back")
                option = input(color_text("Select an option ", "yellow") + alert + "# ")
                
                if option == "0":

                    # Create the chars directory if it doesn't exist
                    if not os.path.exists("chars"):
                        os.makedirs("chars")

                    if os.path.exists(f"chars/{character_class}-starter.json"):
                        option = input(color_text("\nA character with this name already exists. Do you want to overwrite it? ", "red") + alert + "\n0) Yes\n9) No\n# ")
                        if option == "0":
                            file_path = f"chars/{character_class}-starter.json"
                            with open(file_path, "w") as file:
                                json.dump(character, file)
                            return "start"
                        
                        elif option == "9":
                            alert = ""
                            continue
                        else:
                            alert = color_text("\nInvalid input. Please try again. ", "red")
                            continue
                    else:
                        file_path = f"chars/{character_class}.json"
                        with open(file_path, "w") as file:
                            json.dump(character, file)

                        return "start"
                
                elif option == "9":
                    alert = ""
                    continue

        elif option == "1":
            alert = ""

            while True:
                clear()
                print("Character Creation\n")
                name = input(color_text("Enter your character's name ", "yellow") + alert + "\n# ")

                # Check if name is empty or doesn't have at least 3 letters
                if not re.match(r"^[a-zA-Z'.\s]{3,}$", name.strip()) or name.startswith(" ") or name.endswith(" ") or name.startswith("'") or name.endswith("'") or name.startswith(".") or name.endswith("."):
                    alert = color_text(
                        "\nInvalid input. Please enter a valid name. Name must have at least 3 letters and can include letters, apostrophes, periods, and spaces. Name cannot begin or end with a space. ",
                        "red")
                    continue
                else:
                    character_name = name
                    break

            alert = ""

        elif option == "2":
            alert = ""
            character_class = choose_class()

        elif option == "3":
            alert = ""
            attributes, attribute_points = point_distribution(attributes, attribute_points)
            
        elif option == "9":
            option = input(color_text("\nAre you sure you want to cancel? ", "red") + alert + "\n0) Yes\n9) No\n# ")
            if option == "0":
                return "exit"

            elif option == "9":
                alert = ""
                continue

        else:
            alert = color_text("\nInvalid input. Please try again. ", "red")

class Player:

    def __init__(self):
        self.name = name
        self.class_name = player_class
        self.attributes = attributes
        self.attribute_points = attribute_points
        self.level = 1
        self.experience = 0
        self.petos = 0 # Currency
        self.inventory = []
        self.quests = []
        self.location = "home"

        # self.health = 
        # self.mana = 
        # self.stamina = 
    