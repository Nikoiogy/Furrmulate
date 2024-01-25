from game import Game
from utils import Utils

utils = Utils()

def main():
    game = Game(utils)
    game.start()

if __name__ == "__main__":
    main()