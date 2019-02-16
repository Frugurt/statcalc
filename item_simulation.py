# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 18:46:28 2019

@author: Sergei
"""

from numpy import random
from copy import copy
import sys

def progressBar(value, endvalue, bar_length=20, title="Percent:"):
    if endvalue == 0:
        percent = 1.0
    else:
        percent = float(value) / endvalue
    arrow = '-' * int(round(percent * bar_length)-1) + '>'
    spaces = ' ' * (bar_length - len(arrow))

    sys.stdout.write("\r{0:s} [{1}] {2:.2f}%".format(title ,arrow + spaces, percent * 100))
    sys.stdout.flush()
    

class ItemTest:
    def __init__(self):
        self.isoffhand = False
        self.isweapon = False
        self.primary_stats = {}
        self.secondary_stats = {}
        self.n = 4
        self.m = 2
        self.guaranteed = []
        self.desired = []
        
    def good(self, stats, rolls, debug=False):
        if debug:
            print(stats)
            print(rolls)
        rerolls = [self.enchant(stats, des) for des in self.desired]
        verdicts = [self.evaluate(copy(rolls), reroll, des) for reroll, des in zip(rerolls, self.desired)]
        for verdict in verdicts:
            if verdict:
                return True
        return False
    
    def roll_stats(self, isprimal):
        return {}
    
    def pick_stats(self):
        primary = copy(self.primary_stats)
        secondary = copy(self.secondary_stats)
        primary_rolls = self.n
        
        for stat in self.guaranteed:
            if stat in primary:
                del primary[stat]
            if stat in secondary:
                del secondary[stat]
            rolled = [] + self.guaranteed
        ancient = random.randint(1, 11)
        if ancient == 1:
            rolled += ['ancient']
            primal = random.randint(1, 41)
            if primal == 1:
                rolled += ['primal']
                if not self.isoffhand and 'socket' in primary:
                    del primary['socket']
                    if not self.isweapon and 'socket' not in rolled:
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
        if 'AR' in rolled and 'res' in secondary:
            del secondary['res']
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
            if reroll == 'AR' and 'res' in stats:
                return 'RIP'
            if reroll == 'LPH' and 'LPK' in stats:
                return 'RIP'
            return reroll
        
    def evaluate(self, rolls, reroll, desired, debug=False):
        if reroll != 'RIP':
            if reroll in rolls:
                rolls[reroll] = desired[reroll]
            if reroll == 'any':
                for stat in rolls:
                    if stat in desired and (rolls[stat] < desired[stat] and 
                       (stat in self.primary_stats or stat in self.secondary_stats)):
                        rolls[stat] = desired[stat]
                        break
            
            nice = True
            for key in rolls:
                if key in desired and rolls[key] < desired[key]:
                    nice = False
                    break
            if nice:
                if debug:
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
            rolls = self.roll_stats('primal' in stats)
            if self.good(stats, rolls, debug):
                good_sum += 1.0
        self.prob = good_sum / tries
        print("\n")
        if self.prob > 0:
            self.em = 1. / self.prob
            print("On average, one in {:.0f} items has desired stats.".format(self.em))
        else:
            print("No items with desirable stats after {} tries.".format(tries))