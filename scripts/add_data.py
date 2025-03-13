from database.db_connect import create_connection

class AddData:
    def __init__(self):
        self.__connection = create_connection()
        self.__cursor = self.__connection.get_cursor()

    def add_team(self, name: str, league: str):
        checking_request = 'SELECT name FROM Team'
        
        self.__cursor.execute(checking_request)
        team_names = self.__cursor.fetchall()

        for team_name in team_names:
            if name == team_name[0]:
                return 'exists'

        name_request = f'''
            INSERT INTO Team(name)
            VALUES ('{name}')
        '''
        self.__cursor.execute(name_request)
        self.__connection.commit()

        team_id_request = f'''
            SELECT id FROM Team t
            WHERE name == '{name}'
        '''
        self.__cursor.execute(team_id_request)
        team_id = self.__cursor.fetchall()[0][0]

        league_id_request = f'''
            SELECT id FROM League l
            WHERE name == '{league}'
        '''
        self.__cursor.execute(league_id_request)
        league_id = self.__cursor.fetchall()[0][0]

        league_request = f'''
            INSERT INTO LeagueTeam(team_id, league_id)
            VALUES ({int(team_id)}, {int(league_id)})
        '''
        self.__cursor.execute(league_request)
        self.__connection.commit()

        self.__connection.close_connection()

    def add_league(self, name: str):
        checking_request = f'''SELECT name FROM League'''
        self.__cursor.execute(checking_request)
        leag_names = self.__cursor.fetchall()

        for leag_name in leag_names:
            if name == leag_name[0]:
                return 'exists'

        request = f'''
            INSERT  INTO League(name)
            VALUES ('{name}')
        '''

        self.__cursor.execute(request)
        self.__connection.commit()


        self.__connection.close_connection()

def write_game(team_name: str, team_league: str):
    return AddData().add_team(team_name, team_league)

def write_league(leag_name: str):
    return AddData().add_league(leag_name)