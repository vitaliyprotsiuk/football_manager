class League:
    def __init__(self, id, name, teams):
        self.__id = id
        self.__name = name
        self.__teams = teams

    def get_name(self):
        return self.__name
    
    def get_teams(self):
        return self.__teams
    
    def get_id(self):
        return self.__id
    
    def __str__(self):
        return f'{self.__id} {self.__name} {self.__teams}'