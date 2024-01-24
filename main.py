import sys

from menu import Menu
class Game:

    def start(self):
        menu = Menu().main_menu()
        if menu == "start":
            pass
        elif menu == "exit":
            sys.exit()

Game().start()