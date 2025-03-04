import tkinter
import tkinter.messagebox


# from scripts.read_files import read_games, read_teams
from tkinter import ttk
from scripts.tournament import Tournament
from scripts.write_files import write_game
from data.get_data import *


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
        self.__teams = get_teams()
        self.__games = get_games()
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


    def __add_command(self):
        def __get_id_by_team(self, team_name):
            for finded_team in self.__teams:
                if finded_team.get_name() == team_name:
                    return finded_team.get_id()


        def __write_game():
            def __continue_clicked():
                for item in self.__items_adding:
                    item.destroy()

                # updating info for getting last id
#                self.__games = get_games(self.__teams)
#                self.__last_id = __get_last_id(self.__games)

                continue_button.destroy()
                self.__add_command()


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
        

#        self.__last_id = __get_last_id(self.__games)

        def on_team_change(*args):
            return

        self.__home_team_var = tkinter.StringVar(value=self.__teams[0].get_name())
        self.__away_team_var = tkinter.StringVar(value=self.__teams[1].get_name())

        self.__home_team_var.trace_add("write", on_team_change)
        self.__away_team_var.trace_add("write", on_team_change)


        main_label = tkinter.Label(self.__second_tab, text="Введіть дані гри", font=('Arial', 17))
        main_label.grid(row=0)

        team_names_label = tkinter.Label(self.__second_tab, text='Домашня-гостьова команди', font=('Arial', 13))
        team_names_label.grid(row=2, column=0, sticky='w')
        home_name_dropdown = tkinter.OptionMenu(self.__second_tab, self.__home_team_var, *[team.get_name() for team in self.__teams], command=lambda _: on_team_change())
        away_name_dropdown = tkinter.OptionMenu(self.__second_tab, self.__away_team_var, *[team.get_name() for team in self.__teams], command=lambda _: on_team_change())
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
        self.__items_adding = [main_label, home_name_dropdown, away_name_dropdown, team_names_label, away_score_entry, home_score_entry, scores_label, continue_button, date_label, date_entry]