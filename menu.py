# Text RPG

import os
import sys
import json
import re

from utils import clear, color_text, text_speed, color_mode, alert
from player import character_creation

# Main Menu Functions

def main_menu():
    global alert
    clear()
    print("Welcome to the Text RPG!\n")
    print("1) Start")
    print("2) Load")
    print("3) Settings")
    print("\n0) Exit")
    option = input(color_text("Select an option ", "yellow") + alert + "# ")
    if option == "0":
        sys.exit()
    elif option == "1":
        alert = ""
        next_action = character_creation()
        if next_action == "exit":
            main_menu()
        elif next_action == "start":
            # start() # ADD FUNCTIONALITY
    elif option == "2":
        alert = color_text("\nNot yet available! ", "red")
        main_menu()
    elif option == "3":
        alert = ""
        settings()
    else:
        alert = color_text("\nInvalid input. Please try again. ", "red")
        main_menu()


def settings():
    global alert
    global color_mode

    clear()
    print("Settings\n")
    print("In-Game Settings")
    print("1) Change Name")
    print("2) Change Difficulty")
    print("\nAccessability Settings")
    print("3) Color Mode: " + (color_text("On", "green") if color_mode else "Off"))
    print("4) Text Speed: " + text_speed)
    print("\n0) Back")
    option = input(color_text("Select an option ", "yellow") + alert + "# ")
    if option == "0":
        alert = ""
        main_menu()
    elif option == "1":
        alert = color_text("\nNot yet available! ", "red")
        settings()
    elif option == "2":
        alert = color_text("\nNot yet available! ", "red")
        settings()
    elif option == "3":
        color_mode = not color_mode
        alert = ""
        settings()
    elif option == "4":
        alert = color_text("\nNot yet available! ", "red")
        settings()
    else:
        alert = color_text("\nInvalid input. Please try again. ", "red")
        settings()