class Tournament:
    def __init__(self, games, teams):
        self.__games = []
        self.__teams = teams
        for game in games:
            self.add_game(game)
        self.sort_teams()

    def sort_teams(self):
        self.__teams.sort(key=lambda team: team.get_points(), reverse=True)


    def _find_team(self, team):
        for item in self.__teams:
            if item.get_name() == team:
                return item
        return None 


    def add_game(self, game):
        self.__games.append(game)

        homeTeam = self._find_team(game.get_home_team())
        if homeTeam:
            homeTeam.add_game(game)

        awayTeam = self._find_team(game.get_away_team())
        if awayTeam:
            awayTeam.add_game(game)


    def get_list_of_teams(self):
        return [team.get_name() for team in self.__teams]


    def get_list_of_wins(self):
        return [team.get_wins() for team in self.__teams]


    def get_list_of_draws(self):
        return [team.get_draws() for team in self.__teams]


    def get_list_of_loses(self):
        return [team.get_loses() for team in self.__teams]


    def get_list_of_points(self):
        return [team.get_points() for team in self.__teams]
