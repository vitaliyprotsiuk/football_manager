from data.config import *


def write_game(game_id, home_team, away_team, home_team_score, away_team_score):
    with open(GAMES_PATH, 'a') as games:
        games.write(f'\n{game_id} {home_team} {away_team} {home_team_score} {away_team_score}')
        