import json
from tkinter import *
from tkinter.ttk import Combobox




class Heroes():

    def __init__(self):
        self.mas_hero_info = self.get_info_heroes()

    def get_info_heroes(self):
        with open('hero.json', 'r', encoding="utf-8") as j:
            info = json.load(j)
        return info

    def get_names_heroes(self):
        mas_hero = []
        for i in self.mas_hero_info['heros']:
            mas_hero.append(i['name'])
        return mas_hero

class Monsters():

    def __init__(self):
        self.mas_monsters_info = self.get_info_monsters()

    def get_info_monsters(self):
        with open('monster.json', 'r', encoding="utf-8") as j:
            info = json.load(j)
        return info

    def get_names_monsters(self):
        mas_monster = []
        for i in self.mas_monsters_info['monsters']:
            mas_monster.append(i['name'])
        return mas_monster

class SettingsWindow(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        #self.master = master
        #self.pack(fill=BOTH, expand=1)

        self.heroes = Heroes()
        self.selected_heroes = self.heroes.get_names_heroes()

        self.monsters = Monsters()
        self.selected_monsters = []

        self._init_obj_heroes()
        self._init_obj_monsters()

    def _init_obj_monsters(self):
        self.combo_monsters = Combobox(self, state="readonly")
        self.combo_monsters['values'] = self.monsters.get_names_monsters()
        self.combo_monsters.current(0)  # установите вариант по умолчанию
        self.combo_monsters.grid(column=3, row=1)

        self.lbl_monsters = Label(self, text="Монстры", font=("Arial", 18))
        self.lbl_monsters.grid(column=3, row=0)
        self.lbl_selected_monsters = Label(self, text=self.get_selected(self.selected_monsters), font=("Arial", 14))
        self.lbl_selected_monsters.grid(column=3, row=2)

        self.btn_add_delete_monsters = Button(self, text="Добавить/удалить", command=self.clicked_add_delete_monsters)
        self.btn_add_delete_monsters.grid(column=4, row=1)

    def _init_obj_heroes(self):
        self.combo_heroes = Combobox(self, state="readonly")
        self.combo_heroes['values'] = self.heroes.get_names_heroes()
        self.combo_heroes.current(0)  # установите вариант по умолчанию
        self.combo_heroes.grid(column=0, row=1)

        self.lbl_heroes = Label(self, text="Герои", font=("Arial", 18))
        self.lbl_heroes.grid(column=0, row=0)
        self.lbl_selected_heroes = Label(self, text=self.get_selected(self.selected_heroes), font=("Arial", 14))
        self.lbl_selected_heroes.grid(column=0, row=2)

        self.btn_add_delete_heroes = Button(self, text="Добавить/удалить", command=self.clicked_add_delete_heroes)
        self.btn_add_delete_heroes.grid(column=1, row=1)

    def update_selected_heroes(self):
        if self.combo_heroes.get() in self.selected_heroes:
            self.selected_heroes.remove(self.combo_heroes.get())
        else:
            self.selected_heroes.append(self.combo_heroes.get())

    def update_selected_monsters(self):
        if self.combo_monsters.get() in self.selected_monsters:
            self.selected_monsters.remove(self.combo_monsters.get())
        else:
            self.selected_monsters.append(self.combo_monsters.get())

    def get_selected(self, thing):
        result_str = ''
        for i in thing:
            result_str += i + '\n'

        return result_str

    def clicked_add_delete_heroes(self):
        self.update_selected_heroes()
        self.lbl_selected_heroes.configure(text=self.get_selected(self.selected_heroes))

    def clicked_add_delete_monsters(self):
        self.update_selected_monsters()
        self.lbl_selected_monsters.configure(text=self.get_selected(self.selected_monsters))

class MainWindow(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        #self.pack(fill=BOTH, expand=1)
        self.btn_add_delete_monsters = Button(text="открыть настройки", command=self.clicked)
        self.btn_add_delete_monsters.grid(column=4, row=1)

    def clicked(self):
        w = SettingsWindow()



root = Tk()
app = MainWindow(root)
root.title("")
root.geometry('400x250')

root.mainloop()