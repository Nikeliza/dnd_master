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

    def get_info_hero_for_name(self, name):
        for i in range(len(self.mas_hero_info['heros'])):
            if self.mas_hero_info['heros'][i]['name'] == name:
                return self.mas_hero_info['heros'][i]

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
    def __init__(self, sel_monst, sel_her):
        Toplevel.__init__(self)
        #self.master = master
        #self.pack(fill=BOTH, expand=1)

        self.heroes = Heroes()
        self.selected_heroes = sel_her

        self.monsters = Monsters()
        self.selected_monsters = sel_monst

        self._init_obj_heroes()
        self._init_obj_monsters()

    def _init_obj_monsters(self):
        self.combo_monsters = Combobox(self, state="readonly")
        self.combo_monsters['values'] = self.monsters.get_names_monsters()
        self.combo_monsters.current(0)  # установите вариант по умолчанию
        self.combo_monsters.grid(column=3, row=1)

        self.spin_monsters = Spinbox(self, from_=1, to=100)
        self.spin_monsters.grid(column=4, row=1)

        self.lbl_monsters = Label(self, text="Монстры", font=("Arial", 18))
        self.lbl_monsters.grid(column=3, row=0)
        self.lbl_selected_monsters = Label(self, text=self.get_selected_monsters(), font=("Arial", 14))
        self.lbl_selected_monsters.grid(column=3, row=2)


        self.btn_add_delete_monsters = Button(self, text="Добавить/удалить", command=self.clicked_add_delete_monsters)
        self.btn_add_delete_monsters.grid(column=5, row=1)

    def _init_obj_heroes(self):
        self.combo_heroes = Combobox(self, state="readonly")
        self.combo_heroes['values'] = self.heroes.get_names_heroes()
        self.combo_heroes.current(0)  # установите вариант по умолчанию
        self.combo_heroes.grid(column=0, row=1)

        self.lbl_heroes = Label(self, text="Герои", font=("Arial", 18))
        self.lbl_heroes.grid(column=0, row=0)
        self.lbl_selected_heroes = Label(self, text=self.get_selected_heroes(), font=("Arial", 14))
        self.lbl_selected_heroes.grid(column=0, row=2)

        self.btn_add_delete_heroes = Button(self, text="Добавить/удалить", command=self.clicked_add_delete_heroes)
        self.btn_add_delete_heroes.grid(column=1, row=1)

    def update_selected_heroes(self):
        if self.combo_heroes.get() in self.selected_heroes:
            self.selected_heroes.remove(self.combo_heroes.get())
        else:
            self.selected_heroes.append(self.combo_heroes.get())

    def update_selected_monsters(self):
        if self.combo_monsters.get() in self.selected_monsters.keys():
            self.selected_monsters.pop(self.combo_monsters.get())
        else:
            self.selected_monsters[self.combo_monsters.get()] = self.spin_monsters.get()

    def get_selected_heroes(self):
        result_str = ''
        for i in self.selected_heroes:
            result_str += i + '\n'

        return result_str

    def get_selected_monsters(self):
        result_str = ''
        for i in self.selected_monsters:
            result_str += i + ' ' + str(self.selected_monsters[i]) + '\n'

        return result_str

    def clicked_add_delete_heroes(self):
        self.update_selected_heroes()
        self.lbl_selected_heroes.configure(text=self.get_selected_heroes())

    def clicked_add_delete_monsters(self):
        self.update_selected_monsters()
        self.lbl_selected_monsters.configure(text=self.get_selected_monsters())

class MainWindow(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        #self.pack(fill=BOTH, expand=1)
        self.btn_add_delete_monsters = Button(text="открыть настройки", command=self.clicked)
        self.btn_add_delete_monsters.grid(column=4, row=1)

        self.heroes = Heroes()
        self.selected_heroes = self.heroes.get_names_heroes()
        self.battle_heroes = self.selected_heroes

        self.monsters = Monsters()
        self.selected_monsters = {}
        self.battle_monsters = {}

        self.los = Listbox()
        for i in self.selected_heroes:
            self.los.insert(0, i)

        self.los.bind('<<ListboxSelect>>', self.on_select)
        self.los.bind("<Double-Button-1>", self.on_double_click)
        self.los.grid(column=1, row=0)

    def on_double_click(self, event):
        w = InfoWindowHero(self.los.get(self.los.curselection()))


    def on_select(self, event):
        # los.curselection() - получение индекса выделенного элемента
        # los.get() - получение элемента по его индексу
        print(self.los.get(self.los.curselection()))


    def clicked(self):
        self.los.delete(0, len(self.battle_heroes))
        w = SettingsWindow(self.selected_monsters, self.selected_heroes)
        w.wait_window()
        self.battle_heroes = w.selected_heroes
        self.battle_monsters = w.selected_monsters

        for i in self.battle_heroes:
            self.los.insert(0, i)
        print('Selected:', w.selected_monsters, w.selected_heroes)

class InfoWindowHero(Toplevel):
    def __init__(self, name):
        Toplevel.__init__(self)
        #self.master = master
        #self.pack(fill=BOTH, expand=1)

        self.lbl = Label(self, text=name, font=("Arial", 18))
        self.lbl.grid(column=3, row=0)

        self.hero = Heroes().get_info_hero_for_name(name)
        print(self.hero)
        #self.kd = self.heroes['heros'][]

        self.text = Entry(self)
        self.text.insert(0, str(self.hero['KD']))
        self.text.grid(column=4, row=0)







root = Tk()
app = MainWindow(root)
root.title("")
root.geometry('400x250')

root.mainloop()
