from time import sleep
import win32gui
import numpy as np
from .controls import Control
from .window import Window
from .utils import Utils

class Cocapi():
    def __init__(self, name, troops, heroes, spells, loot_goal, dark_elixir_goal, lightning_drills=False):
        self.townhall = None
        self.handle = win32gui.FindWindow(None, f"{name}")
        self.control = Control(self.handle)
        self.window = Window(self.handle)
        self.utils = Utils(self.handle)
        self.window.set_window_size((961, 551))
        self.troops = troops
        self.spells = spells
        self.loot_goal = loot_goal
        self.dark_elixir_goal = dark_elixir_goal
        self.lightning_drills = lightning_drills
        self.heroes = heroes

    def battle_loop(self):
        attack = 0
        while True:
            attack += 1
            self.utils.wait_till_base()
            self.utils.train_troops(self.troops)
            self.utils.brew_spells(self.spells)
            self.utils.wait_for_troops()
            loot = self.utils.look_for_loot(dark_elixir_goal=self.dark_elixir_goal, loot_goal=self.loot_goal)
            if loot[0] + loot[1] >= self.loot_goal:
                self.utils.attack(self.troops, self.heroes["King"], self.heroes["Queen"], self.heroes["Warden"], self.heroes["Champion"])
                self.utils.end_battle_early()
                gains = self.utils.wait_till_battle_over()
            elif loot[2] >= self.dark_elixir_goal:
                if self.utils.lightning_dark_collector():
                    sleep(5)
                    self.utils.end_battle()
                    sleep(2)
                    gains = self.utils.wait_till_battle_over()
                else:
                    self.utils.end_battle()
                    continue
            try:
                print(f"Attack {str(attack)} Complete, Gold: {gains[0]}/{loot[0]}, Elixir: {gains[1]}/{loot[1]}, Dark Elixir: {gains[2]}/{loot[2]}, Trophies: {gains[3]}")
            except:
                pass
            
        


    


    