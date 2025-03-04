from database.db_connect import create_connection
from scripts.game import Game
from scripts.team import Team

def get_games():
    request = 'SELECT * FROM Game'

    connection = create_connection()

    cursor = connection.get_cursor()

    cursor.execute(request)

    games_data = cursor.fetchall()

    games = []

    

    for games_info in games_data:
        home_team_request = f'''
                SELECT name FROM Team
                WHERE id == {games_info[1]}'''
        
        cursor.execute(home_team_request)

        home_team_name = cursor.fetchall()[0]
        home_team_name = home_team_name[0]
        home_team = Team({games_info[1]}, home_team_name)

        away_team_request = f'''
                SELECT name FROM Team
                WHERE id == {games_info[2]}'''
        
        cursor.execute(away_team_request)

        away_team_name = cursor.fetchall()[0]
        away_team_name = away_team_name[0]
        away_team = Team(games_info[2], away_team_name)

        
        date = f'{games_info[5]} {games_info[6]} {games_info[7]}'
        game = Game(games_info[0], home_team, away_team, games_info[3], games_info[4], date)
        
        games.append(game)


    connection.close_connection()

    return games


def get_teams():
    request = 'SELECT id, name FROM Team'

    connection = create_connection()
    cursor = connection.get_cursor()

    cursor.execute(request)

    teams_data = cursor.fetchall()

    teams = []

    for team_info in teams_data:
        team = Team(team_info[0], team_info[1])
        teams.append(team)

    connection.close_connection()

    return teams