from data.config import TEAMS_PATH, GAMES_PATH
from scripts.game import Game
from scripts.team import Team

def read_games(teams: list) -> list:
    games = []
    with open(GAMES_PATH, 'r') as games_file:
        while True:
            line = games_file.readline()
            if line == '':
                break

            array = line.split(' ')
            date = f"{array[5]} {array[6]} {array[7]}"
            game = Game(int(array[0]), find_name_by_id(teams, int(array[1])), find_name_by_id(teams, int(array[2])), int(array[3]), int(array[4]), date)
            games.append(game)
        
        return games


def read_teams() -> list:
    teams = []
    with open(TEAMS_PATH, 'r') as teams_file:
        while True:
            line = teams_file.readline()
            if line == '':
                break

            array = line.split(' ')
            team = Team(int(array[0]), array[1])
            teams.append(team)

        return teams


# additional functions
def find_name_by_id(teams: list, id: int):
    for team in teams:
        if team.get_id() == id:
            return team