import json
from tkinter import *
from tkinter.ttk import Combobox
import random

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

    def get_info_monster_for_name(self, name):
        for i in range(len(self.mas_monsters_info['monsters'])):
            if self.mas_monsters_info['monsters'][i]['name'] == name:
                return self.mas_monsters_info['monsters'][i]



class Monster():
    def __init__(self, monster, count=1):
        self.monster = monster
        self.hit = self.generation_hit()
        self.count = count

    def get_name_with_number(self):
        return self.monster['name'] + ' ' + str(self.count)

    def get_name(self):
        return self.monster['name']

    def generation_hit(self):
        hit = 0
        for i in range(int(self.monster['Hit_ch_k'])):
            hit += random.randint(1, int(self.monster['Hit_num_k']))
        hit += int(self.monster['Hit_plus'])
        return hit

    def get_hit(self):
        return self.hit

    def set_hit(self, hit):
        self.hit = hit


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

        self.mainmenu = Menu(self.master)
        self.master.config(menu=self.mainmenu)
        self.mainmenu.add_command(label='Настройки', command=self.clicked_setting)
        self.mainmenu.add_command(label='Обновить все', command=self.clicked_refresh_all)

        self.heroes = Heroes()
        self.battle_heroes_name = self.heroes.get_names_heroes()
        self.hero_window = {}

        self.monsters = Monsters()
        self.battle_monsters_name = {}
        self.battle_monsters = {}
        self.monster_window = {}

        self._init_obj_heroes()
        self._init_obj_monsters()

    def _init_obj_heroes(self):
        self.lbl_heroes = Label(text='Герои')
        self.lbl_heroes.grid(column=0, row=0)

        self.list_box_heroes = Listbox()
        self.fill_list_box_heroes()
        self.list_box_heroes.bind('<<ListboxSelect>>', self.on_select_hero)
        self.list_box_heroes.bind("<Double-Button-1>", self.on_double_click_hero)
        self.list_box_heroes.grid(column=0, row=1)

    def _init_obj_monsters(self):
        self.lbl_monsters = Label(text='Монстры')
        self.lbl_monsters.grid(column=1, row=0)

        self.list_box_monsters = Listbox()
        self.fill_list_box_monsters()
        self.list_box_monsters.bind('<<ListboxSelect>>', self.on_select_monster)
        self.list_box_monsters.bind("<Double-Button-1>", self.on_double_click_monster)
        self.list_box_monsters.grid(column=1, row=1)

    def fill_list_box_heroes(self):
        for i in self.battle_heroes_name:
            self.list_box_heroes.insert(0, i)

    def fill_list_box_monsters(self):
        for i in self.battle_monsters:
            self.list_box_monsters.insert(0, self.battle_monsters[i].get_name_with_number())

    def on_double_click_hero(self, event):
        name = self.list_box_heroes.get(self.list_box_heroes.curselection())
        try:
            self.hero_window[name].state()
        except:
            self.hero_window[name] = InfoWindowHero(self.heroes.get_info_hero_for_name(name))


    def on_double_click_monster(self, event):
        kost = self.list_box_monsters.get(self.list_box_monsters.curselection())
        try:
            print(self.monster_window[kost].state())
        except:
            self.monster_window[kost] = InfoWindowMonster(self.battle_monsters[kost])

    def on_select_hero(self, event):
        # los.curselection() - получение индекса выделенного элемента
        # los.get() - получение элемента по его индексу
        print(self.list_box_heroes.get(self.list_box_heroes.curselection()))

    def on_select_monster(self, event):
        # los.curselection() - получение индекса выделенного элемента
        # los.get() - получение элемента по его индексу
        print(self.list_box_monsters.get(self.list_box_monsters.curselection()))

    def refresh_battle_monster(self):
        self.battle_monsters = {}
        for i in self.battle_monsters_name:
            for j in range(int(self.battle_monsters_name[i])):
                self.battle_monsters[i + ' ' + str(j + 1)] = Monster(Monsters().get_info_monster_for_name(i), j + 1)

    def clicked_setting(self):
        self.list_box_heroes.delete(0, len(self.battle_heroes_name))
        self.list_box_monsters.delete(0, len(self.battle_monsters_name))
        w = SettingsWindow(self.battle_monsters_name, self.battle_heroes_name)
        w.wait_window()
        self.battle_heroes_name = w.selected_heroes
        self.battle_monsters_name = w.selected_monsters
        self.refresh_battle_monster()

        self.fill_list_box_heroes()
        self.fill_list_box_monsters()

    def clicked_refresh_all(self):
        for i in self.monster_window:
            #print(self.monster_window[i].get_hit())
            #print(self.monster_window[i].get_name())
            print(self.battle_monsters[
                      self.monster_window[i].get_name()
                  ].get_hit())
            #self.battle_monsters[self.monster_window[i].get_name()].set_hit(self.monster_window[i].get_hit())


class InfoWindowHero(Toplevel):
    def __init__(self, hero):
        Toplevel.__init__(self)
        #self.master = master
        #self.pack(fill=BOTH, expand=1)

        self.lbl = Label(self, text=hero['name'], font=("Arial", 18))
        self.lbl.grid(column=3, row=0)

        self.hero = hero
        print(self.hero)
        #self.kd = self.heroes['heros'][]

        self.text = Entry(self)
        self.text.insert(0, str(self.hero['hit']))
        self.text.grid(column=4, row=0)

class InfoWindowMonster(Toplevel):
    def __init__(self, monster):
        Toplevel.__init__(self)
        #self.master = master
        #self.pack(fill=BOTH, expand=1)

        self.lbl = Label(self, text=monster.get_name_with_number(), font=("Arial", 18))
        self.lbl.grid(column=3, row=0)

        self.monster = monster

        self.text = Entry(self)
        self.text.insert(0, str(self.monster.get_hit()))
        self.text.grid(column=4, row=0)

        self.bind('<Return>', self.click_enter)

    def click_enter(self, event):
        self.monster.set_hit(int(self.text.get()))

    def get_name(self):
        return self.monster.get_name_with_number()
    def get_hit(self):
        return self.monster.get_hit()

root = Tk()
app = MainWindow(root)
root.title("")
root.geometry('400x250')

root.mainloop()
