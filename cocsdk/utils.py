from .controls import Control
from .window import Window
from time import sleep
import numpy as np

class Utils():
    def __init__(self, handle):
        self.handle = handle
        self.control = Control(self.handle)
        self.window = Window(self.handle)

    def position(self, corner):
        if corner == "top_left":
            self.control.drag(457, 104, 457, 351)
            sleep(.1)
            self.control.drag(431, 248, 660, 248)
        elif corner == "top_right":
            self.control.drag(457, 104, 457, 351)
            sleep(.05)
            self.control.drag(660, 248, 431, 248)
        elif corner == "bottom_right":
            self.control.drag(457, 351, 457, 104)
            sleep(.05)
            self.control.drag(660, 248, 431, 248)
        elif corner == "bottom_left":
            self.control.drag(457, 351, 457, 104)
            sleep(.05)
            self.control.drag(431, 248, 660, 248)

    def zoom_out(self):
        self.control.scroll(-5, 460, 265, control=True)

    def check_ui(self):
        if not self.window.locate_image("home_base.png", (20, 471, 101, 521)) is False:
            return "home"
        elif not self.window.locate_image("builder_base.png", (20, 471, 101, 521)) is False:
            return "builder"
        
    def wait_till_battle_over(self):
        self.window.wait_for_image("return_home.png", (400, 464, 524, 517))
        sleep(2)
        loot_gained = self.read_loot_gained()
        self.control.click(468, 492)

        return loot_gained

    def wait_till_base(self):
        self.window.wait_for_image("trainbutton.png", (16, 383, 59, 429), click=(8, 538))

    def check_home_townhall(self):
        self.control.click(40, 72)
        self.window.wait_for_image("social.png", (676, 62, 742, 89))

        if self.window.locate_image("townhall_12.png", (148, 464, 297, 539)):
            self.townhall = 12
        elif self.window.locate_image("townhall_11.png", (148, 464, 297, 539)):
            return 11
        elif self.window.locate_image("townhall_10.png", (148, 464, 297, 539)):
            return 10
        
    def quick_train_army_one(self):
        self.control.click(37, 415)
        sleep(.3)

        quick_train = self.window.locate_image("quick_train.png", (510, 49, 833, 93))
        self.control.click(quick_train[0], quick_train[1], relative=False)

        self.control.click(823, 278)

    def end_battle(self):
        # self.window.wait_for_image((11, 397, 124, 342), )
        self.control.click(62, 417)
        sleep(.5)
        self.control.click(561, 358)

    def remove_obstacles(self):
        self.zoom_out()
        self.position("top_left")
        obstacle = self.window.locate_image(image="tree_trunk.png", region=(1, 1, 950, 540), threshold=.8)
        while type(obstacle) != bool:
            self.control.click(obstacle[0], obstacle[1])
            self.control.click(426, 474)
            sleep(.3)
            self.control.click(11, 43)
            sleep(12)
            obstacle = self.window.locate_image(image="tree_trunk.png", region=(1, 1, 950, 540), threshold=.9)

    def read_loot_gained(self):

        gold = int(self.window.read_number((361, 240, 475, 268)))
        elixir = int(self.window.read_number((361, 278, 475, 309)))
        dark_elixir = int(self.window.read_number((361, 312, 475, 343)))
        trophies = int(self.window.read_number((431, 348, 475, 376)))

        return(gold, elixir, dark_elixir, trophies)

    def get_battle_resources(self):

        self.position("top_left")    

        gold = self.window.read_number((49, 98, 130, 113))
        elixir = self.window.read_number((48, 125, 130, 140))
        dark_elixir = self.window.read_number((46, 154, 95, 167))

        if gold == "":
            gold = 0
        if elixir == "":
            elixir = 0
        if dark_elixir == "":
            dark_elixir = 0

            gold = 0
        if int(elixir) > 3000000:
            elixir = 0
        if int(dark_elixir) > 50000:
            dark_elixir = 0
        
        return gold, elixir, dark_elixir

    def end_battle_early(self, interval=15):
        while True:
            check_one = self.get_battle_resources()
            sleep(interval)
            check_two = self.get_battle_resources()
            if check_one == check_two:
                break
        self.end_battle()

    def look_for_loot(self, dark_elixir_goal=5000, loot_goal=1200000):
        self.control.click(62, 486)
        sleep(.5)
        self.control.click(705, 377)
    
        while True:
            self.window.wait_for_image("end_battle.png", (18, 399, 115, 430))

            sleep(.4)
            self.zoom_out()
            sleep(.1)
        
            sleep(.6)
            loot = self.get_battle_resources()
            if (int(loot[0]) + int(loot[1])) >= loot_goal:
                break
            elif int(loot[2]) >= dark_elixir_goal:
                break
            
            self.control.click(803, 404)
        return (int(loot[0]), int(loot[1]), int(loot[2]))

    def train_troops(self, troops):
        """
        PARAMETER TROOPS MUST BE A DICT!!!

        Example:
        troops = {"archer" : 80, "barbarian" : 80, "giant" : 16}
        """
        self.control.click(36, 406)
        sleep(.2)
        self.control.click(269, 60)
        sleep(.4)
        for troop in troops:
            try:
                troop_location = self.window.locate_image(f"{troop}.png", (43, 269, 871, 501))
                for i in range(troops[troop]):
                    self.control.click(troop_location[0], troop_location[1])
                    
            except:
                # print(f"Not enough housing space for {troop}")
                continue
        sleep(.3)
        self.control.click(860, 55)
        sleep(.5)

    def brew_spells(self, spells):
        """
        PARAMETER SPELLS MUST BE A DICT!!!

        Example:
        spells = {"lightning" : 3, "haste" : 1, "jump" : 3}
        """
        self.control.click(36, 406)
        sleep(.2)
        self.control.click(424, 60)
        sleep(.4)
        for spell in spells:
            try:
                spell_location = self.window.locate_image(f"{spell}.png", (43, 269, 871, 501))
                for i in range(spells[spell]):
                    self.control.click(spell_location[0], spell_location[1])
            except:
                # print(f"Not enough housing space for {spell}")
                continue
        self.control.click(860, 55)
        sleep(.5)

    def calculate_placements(self, amount, side):
        if side == "top_left":
            coords = (150, 344, 450, 110)
        elif side == "top_right":
            coords = (478, 121, 773, 341)
        elif side == "bottom_left":
            coords = (133, 166, 437, 390)
        elif side == "bottom_right":
            coords = (788, 180, 479, 400)

        x_locations = np.linspace(coords[0], coords[2], amount)
        y_locations = np.linspace(coords[1], coords[3], amount)

        coords_list = []

        for i in range(len(x_locations)):
            current_coord = (int(x_locations[i]), int(y_locations[i]))
            coords_list.append(current_coord)

        return coords_list

    def select_troop(self, troop):
        try:
            current_troop = self.window.locate_image(f"battle_{troop}.png", (10, 451, 923, 550))
            self.control.click(current_troop[0], current_troop[1])
            sleep(.05)

            return True
        except:
            # print(f"Could not find troop {troop}")
            return False

    def lightning_dark_collector(self):
        attack = False
        if not self.select_troop("lightning"):
            return
        self.zoom_out()
        sleep(.8)
        self.position("bottom_left")
        self.control.drag(300, 100, 300, 150)
        sleep(.4)
        # get positions
        images = ['dark_pump.png', 'dark_pump_2.png', 'dark_pump_3.png']
        full_images = ['dark_pump_high_full_1.png', 'dark_pump_high_full_2.png', 'dark_pump_high_full_3.png']
        locs = self.window.locate_images_all(images, region=[50, 50, 850, 400], threshold=.15)
        for loc in locs:
            self.control.scroll(4, int(loc[0]), int(loc[1]), control=True)
            sleep(.8)
            full_locs = self.window.locate_images_all(full_images, region=[50, 50, 850, 400], threshold=.08)
            if len(full_locs) != 0:
                for i in range(4):
                    self.control.click(int(full_locs[0][0]), int(full_locs[0][1]))
                    attack = True
                    sleep(.1)
            self.zoom_out()
            sleep(.8)
            self.position("bottom_left")
            self.control.drag(300, 100, 300, 150)
            sleep(.8)
        return attack

    def attack(self, troops, king=False, queen=False, warden=False, champion=False):
        """
        PARAMETER TROOPS MUST BE A DICT!!!

        Example:
        troops = {"archer" : 80, "barbarian" : 80, "giant" : 16}
        """
        self.zoom_out()
        self.position("top_left")
        if king or warden:
            self.position("top_left")

            if king and self.select_troop("king"):
                self.control.click(470, 80)
            if warden and self.select_troop("warden"):
                self.control.click(98, 353)
        if champion or queen:
            self.position("bottom_left")

            if champion and self.select_troop("champion"):
                self.control.click(847, 165)
            if queen and self.select_troop("queen"):
                self.control.click(478, 438)

        for troop in troops:

            troops_per_side = (troops[troop] + 1)/4

            top_left_coords = self.calculate_placements(amount=int(troops_per_side), side="top_left")
            top_right_coords = self.calculate_placements(amount=int(troops_per_side), side="top_right")
            bottom_right_coords = self.calculate_placements(amount=int(troops_per_side), side="bottom_right")
            bottom_left_coords = self.calculate_placements(amount=int(troops_per_side), side="bottom_left")

            if not self.select_troop(troop=troop):
                continue

            self.position("top_left")
            for coord in top_left_coords:
                self.control.click(coord[0], coord[1])
            sleep(.05)

            self.position("top_right")
            for coord in top_right_coords:
                self.control.click(coord[0], coord[1])
            sleep(.05)

            self.position("bottom_right")
            for coord in bottom_right_coords:
                self.control.click(coord[0], coord[1])
            sleep(.05)

            self.position("bottom_left")
            for coord in bottom_left_coords:
                self.control.click(coord[0], coord[1])
            self.control.click(498, 422)
            sleep(.05)

            self.position("top_left")
            for coord in top_left_coords:
                self.control.click(coord[0], coord[1])
            sleep(.05)

    def wait_for_troops(self):
        def arguement():
            self.control.click(862, 57)
            sleep(1)
            self.control.click(36, 406)
            sleep(.2)
            self.control.click(269, 60)
            sleep(.4)
            return 1

        self.control.click(36, 406)
        sleep(.2)
        self.control.click(269, 60)
        sleep(.4)

        self.window.wait_for_image_disappear("clock.png", (758, 84, 787, 110), interval=30, function=arguement)

        self.control.click(862, 57)