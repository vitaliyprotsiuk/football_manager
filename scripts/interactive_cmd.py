from scripts.tournament import Tournament
from data.config import GAMES_PATH

class IntCMD:
    __input = None
    __teams = []
    __games = []

    def __init__(self, games, teams):
        self.__games = games
        self.__teams = teams

    def _add_game(self):
        input_table = list(map(int, input("Write the game, like:\n1- game-id 2- home-team-id 3- away-team-id 4- home-team-score 5- away-team-score\n").split(' ')))
        with open(GAMES_PATH, 'a') as game:
            game.write(f"\n{input_table[0]} {input_table[1]} {input_table[2]} {input_table[3]} {input_table[4]}")
        print("DONE✅")

    def cheking(self):
        print("---------Interactive Console---------")
        print("1. Add Game\n2. Print the table")
        self.__input = int(input())
        
        if self.__input == 1:
            self._add_game()

        elif self.__input == 2:
            tournament = Tournament(self.__games, self.__teams)

            tournament.print_table()

        else:
            print("You can choose only 1 or 2")
