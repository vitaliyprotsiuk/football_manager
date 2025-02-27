import tkinter
import tkinter.messagebox


from scripts.read_files import read_games, read_teams
from tkinter import ttk
from scripts.tournament import Tournament
from scripts.write_files import write_game


class Window:
    def __init__(self):
        self.window = tkinter.Tk()
        self.__tab_control = ttk.Notebook(self.window)
        self.__tab_control.bind("<ButtonRelease-1>", self.__update_info) # to update info in table when tab changed
        self.__first_tab = ttk.Frame(self.__tab_control)
        self.__second_tab = ttk.Frame(self.__tab_control)
        self.__table = ttk.Treeview(self.__first_tab, columns=['N', 'W', 'D', 'L', 'P'], show='headings', height=450)

        # addition tabs
        self.__tab_control.add(self.__first_tab, text='Турнірна таблиця')
        self.__tab_control.add(self.__second_tab, text='Додати гру')

        self.__tab_control.grid()

        # start window
        self.manage_window()

    def __update_info(self, event=None):
        for item in self.__table.get_children():
            self.__table.delete(item)
                
        self.__show_table()

        return "break"

    def manage_window(self):
        self.window.title("UEFA Table")
        self.window.geometry("600x400+450+200") # for 1920x1080
        self.window.resizable(False, False)

        self.__show_table()
        self.__add_command()

        self.window.mainloop()


    def __show_table(self):
        self.__teams = read_teams()
        self.__games = read_games(self.__teams)
        games_checked = []

        for game in self.__games:
            if game.get_game_status() == 'InProgress' or game.get_game_status() == 'Finished':
                games_checked.append(game)
        self.tournament = Tournament(games_checked, self.__teams)
        self.__home_team_var = tkinter.StringVar(value=self.__teams[0])
        self.__away_team_var = tkinter.StringVar(value=self.__teams[1])


        def create_table():
            self.__table.heading('N', text='Name')
            self.__table.heading('W', text='W')
            self.__table.heading('D', text='D')
            self.__table.heading('L', text='L')
            self.__table.heading('P', text='P')
            self.__table.column('N', width=120)
            self.__table.column('W', width=120, anchor='center')
            self.__table.column('D', width=120, anchor='center')
            self.__table.column('L', width=120, anchor='center')
            self.__table.column('P', width=120, anchor='center')
            
            for i in range(0, len(self.__teams)):
                names = self.tournament.get_list_of_teams()
                wins = self.tournament.get_list_of_wins()
                draws = self.tournament.get_list_of_draws()
                loses = self.tournament.get_list_of_loses()
                points = self.tournament.get_list_of_points()

                self.__table.insert(parent='', index='end', values=[names[i], wins[i], draws[i], loses[i], points[i]])


            self.__table.grid()

        create_table()


    def __add_command(self):
        def __get_id_by_team(self, team):
            for finded_team in self.__teams:
                if team == finded_team.get_name():
                    return finded_team.get_id()


        def __write_game():
            def __continue_clicked():
                for item in self.__items_adding:
                    item.destroy()

                # updating info for getting last id
                self.__games = read_games(self.__teams)
                self.__last_id = __get_last_id(self.__games)

                continue_button.destroy()
                self.__add_command()


            for inputed in entries:
                try:
                    a = int(inputed.get())
                except:
                    tkinter.messagebox.showerror("Помилка", "Ви ввели не валідні дані")
                    return
                
            game_id = self.__last_id + 1

            write_game(game_id, __get_id_by_team(self, self.__home_team_var.get()), __get_id_by_team(self, self.__away_team_var.get()), home_score_entry.get(), away_score_entry.get())


            for item in self.__items_adding:
                item.destroy()
            
            done_label = tkinter.Label(self.__second_tab, text='Готово✅', font=('Arial', 15))
            done_label.grid(row=0)

            continue_button = tkinter.Button(self.__second_tab, text='Продовжити', font=('Arial', 9), command=__continue_clicked)
            continue_button.grid(row=1)

        
        # get last id
        def __get_last_id(games):
            last_game = games[-1]
            last_id = last_game.get_id()

            return last_id
        

        self.__last_id = __get_last_id(self.__games)


        main_label = tkinter.Label(self.__second_tab, text="Введіть дані гри", font=('Arial', 17))
        main_label.grid(row=0)

        home_name_label = tkinter.Label(self.__second_tab, text='Виберіть назву домашньої команди', font=('Arial', 13))
        home_name_label.grid(row=2, column=0, sticky='w')
        home_name_dropdown = tkinter.OptionMenu(self.__second_tab, self.__home_team_var, *self.__teams)
        home_name_dropdown.grid(row=2, column=1)
        away_name_label = tkinter.Label(self.__second_tab, text='Виберіть назву гостьової команди', font=('Arial', 13))
        away_name_label.grid(row=3, column=0, sticky='w')
        away_name__dropdown = tkinter.OptionMenu(self.__second_tab, self.__away_team_var, *self.__teams)
        away_name__dropdown.grid(row=3, column=1)
        home_score_label = tkinter.Label(self.__second_tab, text='Введіть забиті голи домашньої команди', font=('Arial', 13))
        home_score_label.grid(row=4, column=0, sticky='w')
        home_score_entry = tkinter.Entry(self.__second_tab)
        home_score_entry.grid(row=4, column=1)
        away_score_label = tkinter.Label(self.__second_tab, text='Введіть забиті голи гостьової команди', font=('Arial', 13))
        away_score_label.grid(row=5, column=0, sticky='w')
        away_score_entry = tkinter.Entry(self.__second_tab)
        away_score_entry.grid(row=5, column=1)

        continue_button = tkinter.Button(self.__second_tab, text="Продовжити", command=__write_game)
        continue_button.grid(row=6)

        entries = [home_score_entry, away_score_entry]
        self.__items_adding = [main_label, home_name_dropdown, away_name__dropdown, home_name_label, away_name_label, away_score_entry, away_score_label, home_score_entry, home_score_label, continue_button]