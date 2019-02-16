#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 17 15:06:33 2017

@author: sergey
       boots chest belt
DH      7     5     5
monk    4     5     4 
wiz     7     5     4
WD      5     8     4
necro   3     7     3
sader   6     4     4
barb    4     7     4

"""

from copy import copy

primary = {
    'mainstat':4000,
    'vit':4000,
    'APoC':4000,
    'MS':2000,
    'resource_healing':2000,
    'resource_regen':2000,
    'avg_dmg':1500,
    'dmg%':1000,
    'CC':1000,
    'CHD':1000,
    'CDR':1000,
    'RCR':1000,
    'life':1000,
    'IAS':1000,
    'LPS':1000,
    'AD':1000,
    'AR':1000,
    'armor':1000,
    'LPH':1000,
    'element':1000,
    'socket':1000,
    'skill':1000,
    'CHD_weapon':100,
    'elitedmg':100,
    'eliteres':100,
    'bleed':100
}

secondary = {
    'resource':4000,
    'radius':1500,
    'gold':1000,
    'exp':1000,
    'CCR''':1000,
    'globe':1000,
    'res':6000,
    'LPK':1000,
    'thorns':600,
    'ranged':400,
    'melee':400,
    'level':100,
    'dur':100,
    'fear_helm':200,
    'blind':100,
    'chill':100,
    'freeze':100,
    'slow':100,
    'stun':100,
    'fear':100,
    'knockback':100,
    'immobilize':100
}



chest_primary = {
    'mainstat':4000,
    'vit':4000,
    'life':1000,
    'LPS':1000,
    'AR':1000,
    'armor':1000,
    'socket':1000,
    'skill':5000,
    'eliteres':100,
}

chest_secondary = {
    'radius':1500,
    'gold':1000,
    'exp':1000,
    'globe':1000,
    'res':6000,
    'LPK':1000,
    'thorns':600,
    'ranged':400,
    'melee':400,
    'level':100,
    'dur':100
}

cloak_primary = copy(chest_primary)
cloak_primary['resource_regen'] = primary['resource_regen']
cloak_secondary = copy(chest_secondary)
cloak_secondary['resource'] = secondary['resource']

glove_primary = {
    'mainstat':4000,
    'vit':4000,
    'CC':1000,
    'CHD':1000,
    'CDR':1000,
    'RCR':1000,
    'IAS':1000,
    'LPS':1000,
    'AD':1000,
    'AR':1000,
    'armor':1000,
    'LPH':1000
}

glove_secondary = {
    'radius':1500,
    'gold':1000,
    'exp':1000,
    'res':6000,
    'thorns':600,
    'level':100,
    'dur':100,
    'stun':100
}

bracer_primary = {
    'mainstat':4000,
    'vit':4000,
    'CC':1000,
    'LPS':1000,
    'AR':1000,
    'element':4000,
    'armor':1000,
    'LPH':1000
}

bracer_secondary = {
    'radius':1500,
    'gold':1000,
    'exp':1000,
    'res':6000,
    'thorns':600,
    'ranged':400,
    'melee':400,
    'level':100,
    'dur':100,
    'knockback':100
}

belt_primary = {
    'mainstat':4000,
    'vit':4000,
    'life':1000,
    'LPS':1000,
    'AR':1000,
    'armor':1000,
    'skill':4000,
}

belt_secondary = {
    'radius':1500,
    'LPK':1000,
    'exp':1000,
    'res':6000,
    'thorns':600,
    'ranged':400,
    'melee':400,
    'level':100,
    'dur':100,
    'freeze':100
}

mighty_belt_primary = copy(belt_primary)
mighty_belt_primary['resource_healing'] = primary['resource_healing']
mighty_belt_secondary = copy(belt_secondary)
mighty_belt_secondary['resource'] = secondary['resource']

pants_primary = {
    'mainstat':4000,
    'vit':4000,
    'socket':1000,
    'LPS':1000,
    'AR':1000,
    'armor':1000,
    'skill':4000,
}

pants_secondary = {
    'radius':1500,
    'LPK':1000,
    'exp':1000,
    'res':6000,
    'thorns':600,
    'level':100,
    'dur':100,
    'slow':100
}

shoulder_primary = {
    'mainstat':4000,
    'vit':4000,
    'life':1000,
    'LPS':1000,
    'AR':1000,
    'armor':1000,
    'AD':1000,
    'CDR':1000,
    'RCR':1000,
    'skill':5000,
}

shoulder_secondary = {
    'radius':1500,
    'globe':1000,
    'exp':1000,
    'res':6000,
    'thorns':600,
    'level':100,
    'dur':100,
    'chill':100
}

boots_primary = {
    'mainstat':4000,
    'vit':4000,
    'MS':1000,
    'LPS':1000,
    'AR':1000,
    'armor':1000,
    'skill':7000,
}

boots_secondary = {
    'radius':1500,
    'LPK':1000,
    'exp':1000,
    'res':6000,
    'thorns':600,
    'level':100,
    'dur':100,
    'immobilize':100
}

helmet_primary = {
    'mainstat':4000,
    'vit':4000,
    'CC':1000,
    'life':1000,
    'LPS':1000,
    'AR':1000,
    'armor':1000,
    'LPH':1000,
    'socket':1000,
    'skill':7000,
}


helmet_secondary = {
    'radius':1500,
    'gold':1000,
    'exp':1000,
    'CCR''':1000,
    'res':6000,
    'thorns':600,
    'level':100,
    'dur':100,
    'fear_helm':200,
}

wizard_hat_primary = copy(helmet_primary)
wizard_hat_primary['APoC'] = primary['APoC']
wizard_hat_secondary = copy(helmet_secondary)
wizard_hat_secondary['resource'] = secondary['resource']

voodoo_primary = copy(helmet_primary)
voodoo_primary['resource_regen'] = primary['resource_regen']
voodoo_primary['skill'] = primary['skill'] * 5
voodoo_secondary = copy(wizard_hat_secondary)

spirit_stone_primary = copy(voodoo_primary)
spirit_stone_primary['skill'] = primary['skill'] * 4
spirit_stone_secondary = copy(voodoo_secondary)

weapon_primary = {
    'mainstat':4000,
    'vit':4000,
    'dmg':1000,
    'CDR':1000,
    'RCR':1000,
    'IAS':1000,
    'AD':1000,
    'LPH':1000,
    'socket':1000,
    'elitedmg':100,
    'bleed':100
}

weapon_secondary = {
    'exp':1000,
    'LPK':1000,
    'level':100,
    'dur':100,
    'blind':100,
    'chill':100,
    'freeze':100,
    'slow':100,
    'stun':100,
    'fear':100,
    'knockback':100,
    'immobilize':100
}

wand_primary = copy(weapon_primary)
wand_primary['APoC'] = primary['APoC']
wand_secondary = copy(weapon_secondary)
wand_secondary['resource'] = secondary['resource']

ceremonial_primary = copy(weapon_primary)
ceremonial_primary['resource_regen'] = primary['resource_regen']
ceremonial_secondary = copy(weapon_secondary)
ceremonial_secondary['resource'] = secondary['resource'] / 2 #datamine says mana is different but this needs testing

scythe_secondary = copy(weapon_secondary)
scythe_secondary['resource'] = secondary['resource']

#secondary only for bows/xbows, primary + secondary for hand xbows
bow_primary = copy(weapon_primary)
bow_primary['resource_regen'] = primary['resource_regen']
bow_secondary = copy(weapon_secondary)
bow_secondary['resource'] = secondary['resource']

fist_primary = copy(weapon_primary)
fist_primary['resource_regen'] = primary['resource_regen']
fist_primary['resource_healing'] = primary['resource_healing']
fist_secondary = copy(weapon_secondary)
fist_secondary['resource'] = secondary['resource']

daibo_primary = copy(weapon_primary)
daibo_primary['resource_regen'] = primary['resource_regen']
daibo_primary['resource_healing'] = primary['resource_healing']
daibo_primary['skill'] = primary['skill'] * 13
daibo_secondary = copy(weapon_secondary)
daibo_secondary['resource'] = secondary['resource']

mighty_weapon_primary = copy(fist_primary)
mighty_weapon_secondary = copy(fist_secondary)

big_mighty_weapon_primary = copy(daibo_primary)
big_mighty_weapon_primary['skill'] = primary['skill'] * 15
big_mighty_weapon_secondary = copy(daibo_secondary)

flail_primary = copy(fist_primary)
flail_secondary = copy(fist_secondary)

big_flail_primary = copy(fist_primary)
big_flail_secondary = copy(fist_secondary)

ring_primary = {
    'mainstat':4000,
    'vit':4000,
    'avgdmg':1500,
    'CC':1000,
    'CHD':1000,
    'CDR':1000,
    'RCR':1000,
    'life':1000,
    'IAS':1000,
    'LPS':1000,
    'AD':1000,
    'AR':1000,
    'armor':1000,
    'LPH':1000,
    'socket':1000,
}

ring_secondary = {
    'gold':1000,
    'exp':1000,
    'CCR''':1000,
    'globe':1000,
    'res':6000,
    'LPK':1000,
    'thorns':600,
    'level':100,
    'dur':100,
}

amulet_primary = {
    'mainstat':4000,
    'vit':4000,
    'avgdmg':1500,
    'CC':1000,
    'CHD':1000,
    'CDR':1000,
    'RCR':1000,
    'life':1000,
    'IAS':1000,
    'LPS':1000,
    'AD':1000,
    'AR':1000,
    'armor':1000,
    'element':4000,
    'socket':1000
}

amulet_secondary = {
    'gold':1000,
    'exp':1000,
    'CCR''':1000,
    'globe':1000,
    'res':6000,
    'LPK':1000,
    'thorns':600,
    'ranged':400,
    'melee':400,
    'level':100,
    'dur':100,
    'blind':100
}

offhand_primary = {
    'mainstat':4000,
    'vit':4000,
    'CC':1000,
    'CDR':1000,
    'RCR':1000,
    'life':1000,
    'LPS':1000,
    'AD':1000,
    'socket':1000,
    'skill':17000,
    'elitedmg':100,
    'bleed':100
}

offhand_secondary = {
    'resource':4000,
    'gold':1000,
    'exp':1000,
    'globe':1000,
    'thorns':600,
    'level':100,
    'dur':100,
    'fear':100,
    'blind':100,
    'chill':100,
    'freeze':100,
    'slow':100,
    'stun':100,
    'knockback':100,
    'immobilize':100
}

source_primary = copy(offhand_primary)
source_primary['skill'] = primary['skill'] * 16
source_primary['APoC'] = primary['APoC']

mojo_primary = copy(offhand_primary)
mojo_primary['skill'] = primary['skill'] * 17
mojo_primary['resource_regen'] = primary['resource_regen']

phylactery_primary = copy(mojo_primary)
phylactery_primary['skill'] = primary['skill'] * 13

quiver_primary = copy(mojo_primary)
quiver_primary['skill'] = primary['skill'] * 17

shield_primary = {
    'mainstat':4000,
    'vit':4000,
    'CC':1000,
    'CDR':1000,
    'RCR':1000,
    'life':1000,
    'LPS':1000,
    'block':1000,
    'socket':1000,
    'elitedmg':100,
    'eliteres':100,
    'bleed':100
}

shield_secondary = {
    'res':6000,
    'thorns':600,
    'ranged':400,
    'melee':400,
    'gold':1000,
    'exp':1000,
    'globe':1000,
    'thorns':600,
    'level':100,
    'CCR''':1000,
    'dur':100,
    'fear':100,
    'blind':100,
    'chill':100,
    'freeze':100,
    'slow':100,
    'stun':100,
    'knockback':100,
    'immobilize':100
}

crusader_shield_primary = copy(shield_primary)
crusader_shield_primary['AD'] = primary['AD']
crusader_shield_primary['resource_regen'] = primary['resource_regen']
crusader_shield_primary['resource_healing'] = primary['resource_healing']
crusader_shield_primary['skill'] = primary['skill'] * 14
crusader_shield_secondary = copy(shield_secondary)
crusader_shield_secondary['resource'] = secondary['resource']