import tkinter
import tkinter.messagebox

from tkinter import ttk
from scripts.tournament import Tournament
from data.get_data import *
from scripts.add_data import write_game, write_league


class Window:
    def __init__(self):
        self.window = tkinter.Tk()
        self.__tab_control = ttk.Notebook(self.window)
        self.__tab_control.bind("<ButtonRelease-1>", self.__update_info) # to update info in table when tab changed
        self.__first_tab = ttk.Frame(self.__tab_control)
        self.__second_tab = ttk.Frame(self.__tab_control)
        self.__third_tab = ttk.Frame(self.__tab_control)
        self.__fourth_tab = ttk.Frame(self.__tab_control)
        self.__table = ttk.Treeview(self.__first_tab, columns=['N', 'W', 'D', 'L', 'P'], show='headings', height=450)
        self.__leagues = get_leagues()
        self.__league_names = [leag.get_name() for leag in self.__leagues]
        self.__league_name_var = tkinter.StringVar(value=self.__leagues[0].get_name())

        # addition tabs
        self.__tab_control.add(self.__first_tab, text='Турнірна таблиця')
        self.__tab_control.add(self.__second_tab, text='Додати гру')
        self.__tab_control.add(self.__third_tab, text='Додати команду')
        self.__tab_control.add(self.__fourth_tab, text='Додати лігу')

        self.__tab_control.grid()

        # start window
        self.manage_window()

    def __update_info(self, event=None):
        for item in self.__table.get_children():
            self.__table.delete(item)

        self.__leagues = get_leagues()
        self.__league_names = [leag.get_name() for leag in self.__leagues]

        self.__leagues_optmenu.destroy()

        try:
            for item in self.__extra_game_items:
                item.destroy()
        except:
            pass

        try:
            for item in self.__extra_command_items:
                item.destroy()
        except:
            pass
        
        for item in self.__game_items:
            item.destroy()
        
        for item in self.__command_items:
            item.destroy()

                
        self.__show_table()
        self.__add_command()
        self.__add_game()

        return "break"

    def manage_window(self):
        self.window.title("UEFA Table")
        self.window.geometry("600x400+450+200") # for 1920x1080
        self.window.resizable(False, False)

        self.__show_table()
        self.__add_game()
        self.__add_command()
        self.__add_league()

        self.window.mainloop()


    def __show_table(self):
        self.__leagues_optmenu = tkinter.OptionMenu(self.__first_tab, self.__league_name_var, *[leag_name.get_name() for leag_name in self.__leagues], command=self.__update_info)
        self.__leagues_optmenu.grid(row=0, column=0)

        league_name = self.__league_name_var.get()
        self.__league = self.__leagues[0]
        if len(self.__leagues) > 1:
            for i in range(1, len(self.__leagues)):
                if self.__leagues[i].get_name() == league_name:
                    self.__league = self.__leagues[i]
                    break
                else: continue

        team_names = self.__league.get_teams()
        teams = get_teams()
        self.__teams = []

        for team_name in team_names:
            teams_names = [team.get_name() for team in teams]

            for team in teams:
                if team.get_name() == team_name:
                    self.__teams.append(team)
                    break

        games = get_games()
        self.__games = []

        for game in games:
            tn = [team.get_name() for team in self.__teams]
            if game.get_home_team().get_name() in tn \
            and game.get_away_team().get_name() in tn:
                self.__games.append(game)

        games_checked = []
        for game in self.__games:
            if game.get_game_status() == 'InProgress' or game.get_game_status() == 'Finished':
                games_checked.append(game)
                
        self.tournament = Tournament(games_checked, self.__teams)

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


    def __add_game(self):
        def __get_id_by_team(self, team_name):
            for finded_team in self.__teams:
                if finded_team.get_name() == team_name:
                    return finded_team.get_id()


        def __write_game():
            def __continue_clicked():
                for item in self.__game_items:
                    item.destroy()
                    
                continue_button.destroy()
                self.__add_game()


            for inputed in entries:
                try:
                    a = int(inputed.get())
                    if a < 0:
                        tkinter.messagebox.showerror("Помилка", "Ви ввели не валідні дані")
                        return
                except:
                    tkinter.messagebox.showerror("Помилка", "Ви ввели не валідні дані")
                    return
            
            month_limites = {
                1: 31,
                2: 28,
                3: 31,
                4: 30,
                5: 31,
                6: 30,
                7: 31,
                8: 31,
                9: 30,
                10: 31,
                11: 30,
                12: 31
            }

            try:
                date = date_entry.get().split(" ")
                for num in date:
                    num = int(num)
                
                date = [int(date[0]), int(date[1]), int(date[2])]

                if date[0] < 0 or date[0] > 2100:
                    tkinter.messagebox.showerror("Помилка", "Ви ввели неправильний рік")
                    return
                if date[1] <= 0 or date[1] > 12:
                    tkinter.messagebox.showerror("Помилка", "Ви ввели неправильний місяць")
                    return
                if date[2] < 0 or date[2] > month_limites[date[1]]:
                    tkinter.messagebox.showerror("Помилка", "Ви ввели неправильний день")
                    return
            except ValueError:
                tkinter.messagebox.showerror("Помилка", "Ви ввели неправильний день")
                return
            
#            game_id = self.__last_id + 1

            date = f'{date[0]} {date[1]} {date[2]}'

#            write_game(game_id, __get_id_by_team(self, self.__home_team_var.get()), __get_id_by_team(self, self.__away_team_var.get()), home_score_entry.get(), away_score_entry.get(), date)

            new_game = Game(None, __get_id_by_team(self, self.__home_team_var.get()), __get_id_by_team(self, self.__away_team_var.get()), home_score_entry.get(), away_score_entry.get(), date)
            new_game.add_game()
            self.__teams = get_teams()

            for item in self.__game_items:
                item.destroy()
            
            done_label = tkinter.Label(self.__second_tab, text='Готово✅', font=('Arial', 15))
            done_label.grid(row=0)

            continue_button = tkinter.Button(self.__second_tab, text='Продовжити', font=('Arial', 9), command=__continue_clicked)
            continue_button.grid(row=1)

            self.__extra_game_items = [done_label, continue_button]

        
        # get last id
        def __get_last_id(games):
            last_game = games[-1]
            last_id = last_game.get_id()

            return last_id
        

#        self.__last_id = __get_last_id(self.__games)

        def on_team_change(*args):
            return

        self.__home_team_var = tkinter.StringVar(value=get_teams()[0].get_name())
        self.__away_team_var = tkinter.StringVar(value=get_teams()[1].get_name())

        self.__home_team_var.trace_add("write", on_team_change)
        self.__away_team_var.trace_add("write", on_team_change)


        main_label = tkinter.Label(self.__second_tab, text="Введіть дані гри", font=('Arial', 17))
        main_label.grid(row=0)

        team_names_label = tkinter.Label(self.__second_tab, text='Домашня-гостьова команди', font=('Arial', 13))
        team_names_label.grid(row=2, column=0, sticky='w')
        home_name_dropdown = tkinter.OptionMenu(self.__second_tab, self.__home_team_var, *[team.get_name() for team in get_teams()], command=lambda _: on_team_change())
        away_name_dropdown = tkinter.OptionMenu(self.__second_tab, self.__away_team_var, *[team.get_name() for team in get_teams()], command=lambda _: on_team_change())
        home_name_dropdown.grid(row=2, column=1)
        away_name_dropdown.grid(row=2, column=2)
        scores_label = tkinter.Label(self.__second_tab, text='Голи домашньої-гостьової команд', font=('Arial', 13))
        scores_label.grid(row=3, column=0, sticky='w')
        home_score_entry = tkinter.Entry(self.__second_tab, width=7)
        home_score_entry.grid(row=3, column=1)
        away_score_entry = tkinter.Entry(self.__second_tab, width=7)
        away_score_entry.grid(row=3, column=2)
        date_label = tkinter.Label(self.__second_tab, text='Дата гри(приклад: 2025 3 20)', font=('Arial', 13))
        date_label.grid(row=4, column=0, sticky='w')
        date_entry = tkinter.Entry(self.__second_tab, width=10)
        date_entry.grid(row=4, column=1)

        continue_button = tkinter.Button(self.__second_tab, text="Продовжити", command=__write_game)
        continue_button.grid(row=5)

        entries = [home_score_entry, away_score_entry]
        self.__game_items = [main_label, home_name_dropdown, away_name_dropdown, team_names_label, away_score_entry, home_score_entry, scores_label, continue_button, date_label, date_entry]


    def __add_command(self):
        # Continue button clicked function
        def continue_clicked():
            def repeat():
                done_label.destroy()
                repeat_button.destroy()
                
                self.__add_command()
                

            team_name = name_enrty.get()
            league_name = league_name_var.get()

            if write_game(team_name, league_name) == 'exists':
                tkinter.messagebox.showerror('Помилка', 'Команда з такою назвою вже існує')
                return

            for item in self.__command_items:
                item.destroy()

            done_label = tkinter.Label(self.__third_tab, text='Готово✅', font=('Arial', 15))
            done_label.grid(row=0, column=0)

            repeat_button = tkinter.Button(self.__third_tab, text='Продовжити', command=repeat)
            repeat_button.grid(row=1)

            self.__extra_command_items = [done_label, repeat_button]


        league_name_var = tkinter.StringVar(value=self.__leagues[0].get_name())

        # UI
        name_label = tkinter.Label(self.__third_tab, text='Назва команди', font=('Arial', 13))
        name_label.grid(row=0, column=0)
        name_enrty = tkinter.Entry(self.__third_tab, width=10, justify='center')
        name_enrty.grid(row=0, column=1)

        league_label = tkinter.Label(self.__third_tab, text='Ліга', font=('Arial', 13))
        league_label.grid(row=1, column=0)
        league_drop = tkinter.OptionMenu(self.__third_tab, league_name_var, *self.__league_names)
        league_drop.grid(row=1, column=1)

        continue_button = tkinter.Button(self.__third_tab, text='Продовжити', command=continue_clicked, justify='center')
        continue_button.grid(row=2)

        self.__command_items = [name_enrty, name_label, league_drop, league_label, continue_button]


    def __add_league(self):
        def continue_clicked():
            def repeat():
                done_label.destroy()
                repeat_button.destroy()
                
                self.__add_league()

            league_name = league_name_entry.get()

            if write_league(league_name) == 'exists':
                tkinter.messagebox.showerror('Помилка', 'Ліга з такою назвою вже існує')
                return

            for item in items:
                item.destroy()

            done_label = tkinter.Label(self.__fourth_tab, text='Готово✅', font=('Arial', 15))
            done_label.grid(row=0, column=0)

            repeat_button = tkinter.Button(self.__fourth_tab, text='Продовжити', command=repeat)
            repeat_button.grid(row=1)
            

        # UI
        league_name_label = tkinter.Label(self.__fourth_tab, text='Назва ліги', font=('Arial', 13))
        league_name_label.grid(row=0)
        league_name_entry = tkinter.Entry(self.__fourth_tab)
        league_name_entry.grid(row=0, column=1)

        continue_button = tkinter.Button(self.__fourth_tab, text='Продовжити', command=continue_clicked)
        continue_button.grid(row=1)

        items = [league_name_entry, league_name_label, continue_button]