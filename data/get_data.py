from database.db_connect import connect_db
from scripts.game import Game
from scripts.team import Team

def get_games():
    request = 'SELECT * FROM Game'

    cursor = connect_db()

    cursor.execute(request)

    games_data = cursor.fetchall()

    games = []

    for games_info in games_data:
        date = f'{games_info[5]} {games_info[6]} {games_info[7]}'
        game = Game(games_info[0], games_info[1], games_info[2], games_info[3], games_info[4], date)
        
        games.append(game)


    return games


def get_teams():
    request = 'SELECT * FROM Team'

    cursor = connect_db()

    cursor.execute(request)

    teams_data = cursor.fetchall()

    teams = []

    for team_info in teams_data:
        team = Team(team_info[0], team_info[1])
        teams.append(team)

    return teams