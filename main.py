# Text RPG

import os
import sys
import json
import re

# Define Variables
info = ""
color_mode = True
text_speed = "Normal"
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


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    global info
    clear()
    print("Welcome to the Text RPG!")
    print("1) Start")
    print("2) Load")
    print("3) Settings")
    print("4) Exit")
    option = input(info + "# ")
    if option == "1":
        info = ""
        character_creation()
    elif option == "2":
        info = "Not yet available! "
        main_menu()
    elif option == "3":
        settings()
    elif option == "4":
        sys.exit()
    else:
        info = "Invalid input. Please try again. "
        main_menu()

def settings():
    global info
    global color_mode
    
    info = ""
    clear()
    print("Settings\n")
    print("In-Game Settings")
    print("1) Change Name")
    print("2) Change Difficulty")
    print("\nAccessability Settings")
    print("3) Color Mode: " + ("On" if color_mode else "Off"))
    print("4) Text Speed: " + text_speed)
    print("\n5) Back")
    option = input(info + "# ")
    if option == "1":
        info = "Not yet available! "
        settings()
    elif option == "2":
        info = "Not yet available! "
        settings()
    elif option == "3":
        color_mode = not color_mode
        settings()
    elif option == "4":
        info = "Not yet available! "
        settings()
    elif option == "5":
        main_menu()
    else:
        info = "Invalid input. Please try again. "
        settings()

# Character Creation Functions    

def point_distribution():
    global info
    global attributes
    global attribute_points

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
        print("\n"+descriptions[attribute_name])

    while attribute_points > 0:
        clear()
        print("Point Distribution\n")
        print("You have", attribute_points, "points remaining.")
        print("1) Strength:", attributes["Strength"])
        print("2) Intelligence:", attributes["Intelligence"])
        print("3) Willpower:", attributes["Willpower"])
        print("4) Agility:", attributes["Agility"])
        print("5) Endurance:", attributes["Endurance"])
        print("6) Charisma:", attributes["Charisma"])
        print("7) Luck:", attributes["Luck"])
        print("\n0) Done")

        option = input(f"\033[33m{info}\033[0m# ")

        if option == "0":
            break
        elif option in ["1", "2", "3", "4", "5", "6", "7"]:
            attribute_name = list(attributes.keys())[int(option) - 1]
            try:
                print_attribute_description(attribute_name)
                value = int(input("Enter the new value for " + attribute_name + "\n# "))
                if value < 0 or value > attribute_points:
                    info = "Invalid input. Please enter a valid number between 0 and " + str(attribute_points) + ". "
                else:
                    attribute_points += attributes[attribute_name] - value
                    attributes[attribute_name] = value
                    info = ""
            except ValueError:
                info = "Invalid input. Please enter a valid number. "
        else:
            info = "Invalid input. Please try again. "

    return attributes

def character_creation():
    global info

    def print_class_description(class_name):
        descriptions = {
            "Warrior": "A strong and skilled fighter who excels in close combat.",
            "Mage": "A master of magic who can cast powerful spells.",
            "Rogue": "A stealthy and agile character who specializes in sneak attacks."
        }
        print("\n"+descriptions[class_name])

    clear()

    while True:
        clear()
        print("Character Creation\n")

        print("1) Choose Name")
        print("2) Choose Class")
        print("3) Point Distribution")
        print("\n0) Done")

        option = input(f"\033[33m{info}\033[0m# ")

        if option == "0":
            break
        elif option == "1":
            info = ""

            clear()
            print("Character Creation\n")
            print("Please enter your character's name:")
            name = input(f"\033[33m{info}\033[0m# ")

            # Check if name is empty or doesn't have at least 3 letters
            if not re.match(r"^[a-zA-Z'.]{3,}$", name):
                info = "Invalid input. Please enter a valid name. Name must have at least 3 letters and can include letters, apostrophes, and periods. "
                continue
            
            info = ""

        elif option == "2":
            info = ""

            clear()
            print("Character Creation\n")
            print("Please choose your character's class:")
            print("1) Warrior")
            print("2) Mage")
            print("3) Rogue")
            class_option = input(f"\033[33m{info}\033[0m# ")
            if class_option == "1":
                character_class = "Warrior"
            elif class_option == "2":
                character_class = "Mage"
            elif class_option == "3":
                character_class = "Rogue"
            else:
                info = "Invalid input. Please try again. "
                continue
            print_class_description(character_class)
            class_confirmation = input("Choose this class? \n1) Yes \n2) No \n# ")
            if class_confirmation == "2":
                continue
        elif option == "3":
            info = ""
            attributes = point_distribution()
        else:
            info = "Invalid input. Please try again. "

main_menu()