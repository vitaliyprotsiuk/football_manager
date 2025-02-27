class Game:
    __homeTeam = None
    __awayTeam = None
    __homeTeamScore = 0
    __awayTeamScore = 0

    def __init__(self, id, homeTeam, awayTeam, homeTeamScore, awayTeamScore):
        self.__id = id
        self.__homeTeam = homeTeam
        self.__awayTeam = awayTeam
        self.__homeTeamScore = homeTeamScore
        self.__awayTeamScore = awayTeamScore

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

    def __str__(self):
        return f"{self.__homeTeam} {self.__homeTeamScore} - {self.__awayTeam} {self.__awayTeamScore}"