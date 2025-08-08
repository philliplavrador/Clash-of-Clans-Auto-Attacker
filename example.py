from cocapi import Cocapi
import time

troops = {'miner': 42}
spells = {"lightning": 11}
heroes = {"King": True, "Queen": True, "Warden": True, "Champion": False}
dark_elixir_goal = 6000
loot_goal = 1200000
attacks = 0
client_1 = Cocapi("Apollo", troops, heroes, spells, loot_goal, dark_elixir_goal)
client_1.battle_loop()