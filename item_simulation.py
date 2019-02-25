# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 18:46:28 2019

@author: Sergei
"""

import argparse
from numpy import random
import numpy as np
from copy import copy
import sys
import os
import json

directory = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(directory, "primary_affixes.json")) as f:
   affix_primary = json.load(f)

with open(os.path.join(directory, "secondary_affixes.json")) as f:
   affix_secondary = json.load(f)
   
with open(os.path.join(directory, "primary_types.json")) as f:
   types_primary = json.load(f)
   
with open(os.path.join(directory, "secondary_types.json")) as f:
   types_secondary = json.load(f)
   
with open(os.path.join(directory, "multi.json")) as f:
   multi_data = json.load(f)

def progressBar(value, endvalue, bar_length=20, title="Percent:"):
    if endvalue == 0:
        percent = 1.0
    else:
        percent = float(value) / endvalue
    arrow = '-' * int(round(percent * bar_length)-1) + '>'
    spaces = ' ' * (bar_length - len(arrow))

    sys.stdout.write("\r{0:s} [{1}] {2:.2f}%".format(title ,arrow + spaces, percent * 100))
    sys.stdout.flush()

class Affix(object):
    def __init__(self, name, weight, increment, min_regular, max_regular, min_ancient, max_ancient, multi, reroll):
        self._name = name
        self._weight = weight
        self._increment = increment
        self._min_regular = min_regular
        self._max_regular = max_regular
        self._min_ancient = min_ancient
        self._max_ancient = max_ancient
        self._multi = multi
        self._reroll = True
        
    def roll(self, isancient, isprimal):
        multi = random.randint(1, self._multi + 1)
        if not isancient:
            n_states = int(np.around((self._max_regular - self._min_regular) / self._increment)) + 1
            rng = random.randint(0, n_states)
            value = self._min_regular + rng * self._increment
        else:
            n_states = int(np.around((self._max_ancient - self._min_ancient) / self._increment)) + 1
            rng = random.randint(0, n_states)
            value = self._min_ancient + rng * self._increment
            if isprimal:
                value = self._max_ancient
        return self._name, value, multi

class ItemTest:
#    def __init__(self):
#        self.isoffhand = False
#        self.isweapon = False
#        self.primary_stats = {}
#        self.secondary_stats = {}
#        self.n = 4
#        self.m = 2
#        self.guaranteed = []
#        self.desired = []
    def __init__(self, filename):
        with open(filename) as f:
            data = json.load(f)
        self.name = data["name"]
        self.d3class = data["class"]
        i_type = data["stats"]["type"]
        i_subtype = data["stats"]["subtype"]
        
        primary_list = types_primary[i_type]["affixes"]
        if i_subtype is not None and i_subtype in types_primary[i_type]:
            primary_list += types_primary[i_type][i_subtype]
        self.primary_stats = {}
        if "avgdmg" in primary_list:
            primary_list += ["min_damage", "max_damage"]
        for stat in primary_list:
            weight = affix_primary[stat]["weight"]
            increment = affix_primary[stat]["increment"]
            multi = affix_primary[stat]["multi"]
            if stat in multi_data["by_class"]:
                for el in multi_data["by_class"][stat]:
                    if i_type in el["type"]:
                        multi = el["stats"][self.d3class]
            if stat in multi_data["by_slot"] and i_type in multi_data["by_slot"][stat]:
                multi = multi_data["by_slot"][stat][i_type]
            for statrange in affix_primary[stat]["ranges"]:
                if i_type in statrange["type"] or i_subtype in statrange["type"]:
                    min_regular = statrange["min"]
                    max_regular = statrange["max"]
                    min_ancient = statrange["ancient_min"]
                    max_ancient = statrange["ancient_max"]
                    break
            self.primary_stats[stat] = Affix(stat, weight, increment, min_regular, max_regular, min_ancient, max_ancient, multi, True)
        self.guaranteed_primary = []
        for stat in data["stats"]["guaranteed_primary"]:
            if "special" in stat and stat["special"]:
                self.primary_stats[stat["affix"]] = Affix(stat["affix"], 0, 1, stat["min"], stat["max"], stat["min"], stat["max"], stat["multistat"], stat["reroll"])
            self.guaranteed_primary += [stat["affix"]]
            
        secondary_list = types_secondary[i_type]["affixes"]
        if i_subtype is not None and i_subtype in types_secondary[i_type]:
            secondary_list += types_secondary[i_type][i_subtype]
        self.secondary_stats = {}
        for stat in secondary_list:
            weight = affix_secondary[stat]["weight"]
            increment = affix_secondary[stat]["increment"]
            multi = affix_secondary[stat]["multi"]
            if stat in multi_data["by_class"]:
                for el in multi_data["by_class"][stat]:
                    if i_type in el["type"]:
                        multi = el["stats"][self.d3class]
            if stat in multi_data["by_slot"] and i_type in multi_data["by_slot"][stat]:
                multi = multi_data["by_slot"][stat][i_type]
            for statrange in affix_secondary[stat]["ranges"]:
                if i_type in statrange["type"] or i_subtype in statrange["type"]:
                    min_regular = statrange["min"]
                    max_regular = statrange["max"]
                    min_ancient = statrange["ancient_min"]
                    max_ancient = statrange["ancient_max"]
                    break
            self.secondary_stats[stat] = Affix(stat, weight, increment, min_regular, max_regular, min_ancient, max_ancient, multi, True)
        self.guaranteed_secondary = []
        for stat in data["stats"]["guaranteed_secondary"]:
            if "special" in stat and stat["special"]:
                self.secondary_stats[stat["affix"]] = Affix(stat["affix"], 0, 1, stat["min"], stat["max"], stat["min"], stat["max"], stat["multistat"], stat["reroll"])
            self.guaranteed_secondary += [stat["affix"]]
        self.desired = data["stats"]["desired_rolls"]
        
        self.n = data["stats"]["num_primary"] - len(self.guaranteed_primary)
        self.m = data["stats"]["num_secondary"] - len(self.guaranteed_secondary)
        
        self.item_type = i_type
        self.subtype = i_subtype
        
        if self.subtype == "quiver":
            self.primary_stats["IAS"]._reroll = False
        if self.item_type == "shield":
            self.primary_stats["native_block"]._reroll = False
        if self.subtype in ["source", "mojo", "phylactery"]:
            self.primary_stats["avgdmg"]._reroll = False
        
        
        
    def good(self, stats, rolls, debug=False):
        #if debug:
        #    print(stats)
        #    print(rolls)
        rerolls = []
        for conf in self.desired:
            needed = list(conf["configuration"].keys())
            if conf["ancient"]:
                needed += ["ancient"]
            rerolls += [self.enchant(stats, needed)]
        verdicts = [self.evaluate(copy(rolls), reroll, des, debug) for reroll, des in zip(rerolls, self.desired)]
        for verdict in verdicts:
            if verdict:
                return True
        return False
    
    def roll_stats(self, stats):
        rolls = {}
        isancient = "ancient" in stats
        isprimal = "primal" in stats
        for stat in stats:
            if stat == "avgdmg":
                min_roll = self.primary_stats["min_damage"].roll(isancient, isprimal)
                max_roll = self.primary_stats["max_damage"].roll(isancient, isprimal)
                roll = (stat, min_roll[1] + max_roll[1], 1)
            elif stat in self.primary_stats:
                roll = self.primary_stats[stat].roll(isancient, isprimal)
                if stat == "socket" and "socket" in self.guaranteed_primary:
                    roll = self.primary_stats[stat].roll(True, True)
            elif stat in self.secondary_stats:
                roll = self.secondary_stats[stat].roll(isancient, isprimal)
            else:
                roll = (stat, 0, 0)
            rolls[roll[0]] = (roll[1], roll[2])
        return rolls
        
    
    def pick_stats(self):
        primary = {k:self.primary_stats[k]._weight * self.primary_stats[k]._multi for k in self.primary_stats.keys()}
        secondary = {k:self.secondary_stats[k]._weight * self.secondary_stats[k]._multi for k in self.secondary_stats.keys()}
        primary_rolls = self.n
        
        for stat in self.guaranteed_primary:
            if stat in primary:
                del primary[stat]
        for stat in self.guaranteed_secondary:
            if stat in secondary:
                del secondary[stat]
        rolled = [] + self.guaranteed_primary + self.guaranteed_secondary
        ancient = random.randint(1, 11)
        if ancient == 1:
            rolled += ['ancient']
            primal = random.randint(1, 41)
            if primal == 1:
                rolled += ['primal']
                if self.item_type != "offhand" and self.item_type != "shield" and 'socket' in primary:
                    del primary['socket']
                    if (self.item_type != "1h") and (self.item_type != "2h") and ('socket' not in rolled):
                        rolled += ['socket']
                        primary_rolls -= 1

        for i in range(primary_rolls):
            total_weight = sum([primary[key] for key in primary])
            rng = random.randint(0, total_weight)
            weight_sum = 0
            for stat in primary:
                weight_sum += primary[stat]
                if weight_sum >= rng:
                    rolled += [stat]
                    del primary[stat]
                    break
        if 'AR' in rolled and 'resist' in secondary:
            del secondary['resist']
        if 'LPH' in rolled and 'LPK' in secondary:
            del secondary['LPK']
        for i in range(self.m):
            total_weight = sum([secondary[key] for key in secondary])
            rng = random.randint(0, total_weight)
            weight_sum = 0
            for stat in secondary:
                weight_sum += secondary[stat]
                if weight_sum >= rng:
                    rolled += [stat]
                    del secondary[stat]
                    break
        return rolled
    
    def enchant(self, stats, needed):
        hits = 0
        for stat in needed:
            if stat in stats:
                hits += 1
            else:
                reroll = stat
        if hits < len(needed) - 1:
            return 'RIP'
        if hits == len(needed):
            return 'any'
        if hits == len(needed) - 1:
            if reroll == 'AR' and 'resist' in stats:
                return 'RIP'
            if reroll == 'LPH' and 'LPK' in stats:
                return 'RIP'
            return reroll
    #rolls - dict statname:(value, multi)
    #rerolls - string single stat or any or RIP
    #desired one elemnt of desired list   
    def evaluate(self, rolls, reroll, desired, debug=False):
        if reroll != 'RIP' and reroll != 'ancient':
            if reroll in rolls:
                rolls[reroll] = (desired["configuration"][reroll]["min"], desired["configuration"][reroll]["multistat_order"])
            if reroll == 'any':
                for stat in rolls:
                    if stat in desired["configuration"] and (rolls[stat][0] < desired["configuration"][stat]["min"] or rolls[stat][1] < desired["configuration"][stat]["multistat_order"]):
                        if (stat in self.primary_stats and self.primary_stats[stat]._reroll) or (stat in self.secondary_stats and self.secondary_stats[stat]._reroll):
                            rolls[stat] = (desired["configuration"][stat]["min"], desired["configuration"][stat]["multistat_order"])
                            break
            
            nice = True
            for key in rolls:
                if key in desired["configuration"] and (rolls[key][0] < desired["configuration"][key]["min"] or rolls[key][1] < desired["configuration"][key]["multistat_order"]):
                    nice = False
                    break
            if nice:
                if debug:
                    print(reroll)
                    print(rolls)
                return True
        return False
    
    def minitest(self, debug=False):
        stats = self.pick_stats()
        rolls = self.roll_stats()
        print(stats)
        print(rolls)
        print(self.enchant(stats, self.desired[0]))
        print(self.good(stats, rolls, debug))
       
    def test(self, tries=100000, debug=False):
        good_sum = 0.0
        for i in range(tries): 
            if i % (tries // 2000 + 1) == 0 and not debug:
                progressBar(i, tries-1, bar_length=40, title="Simulating:")
            stats = self.pick_stats()
            rolls = self.roll_stats(stats)
            if self.good(stats, rolls, debug):
                good_sum += 1.0
        self.prob = good_sum / tries
        print("\n")
        if self.prob > 0:
            self.em = 1. / self.prob
            print("On average, one in {:.0f} items has desired stats.".format(self.em))
        else:
            print("No items with desirable stats after {} tries.".format(tries))
            
def main():
    parser = argparse.ArgumentParser(description='Determines rarity of items in d3 via MC simulation')
    parser.add_argument('input_file', type=str, help='JSON file with item data')
    parser.add_argument('--tries', type=int, default=100000, help='Number of items to roll', metavar='N')

    args = parser.parse_args()
    
    ItemTest(args.input_file).test(args.tries)
    
if __name__ == '__main__':  
    main()  