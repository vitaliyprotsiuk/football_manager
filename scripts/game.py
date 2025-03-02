from datetime import date

class Game:
    __homeTeam = None
    __awayTeam = None
    __homeTeamScore = 0
    __awayTeamScore = 0
    __date = None

    def __init__(self, id, homeTeam, awayTeam, homeTeamScore, awayTeamScore, match_date):
        self.__id = id
        self.__homeTeam = homeTeam
        self.__awayTeam = awayTeam
        self.__homeTeamScore = homeTeamScore
        self.__awayTeamScore = awayTeamScore
        match_date = match_date.split(' ')
        match_date = [int(match_date[0]), int(match_date[1]), int(match_date[2])]
        self.__date = date(match_date[0], match_date[1], match_date[2])

    def get_home_team(self):
        return self.__homeTeam

    def get_away_team(self):
        return self.__awayTeam
    
    def get_home_team_score(self):
        return self.__homeTeamScore

    def get_away_team_score(self):
        return self.__awayTeamScore
    
    def get_id(self):
        return self.__id
    
    def get_date(self):
        return self.__date
    
    def get_game_status(self) -> str:
        if self.__date > date.today():
            return 'Scheduled'
        elif self.__date == date.today():
            return 'InProgress'
        else: return 'Finished'
    
    def __str__(self):
        return f"{self.__homeTeam} {self.__homeTeamScore} - {self.__awayTeam} {self.__awayTeamScore}"