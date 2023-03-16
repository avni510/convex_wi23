import math
import numpy as np
import json
from urllib.request import urlopen

##############################################################################################
# Starting Code for generating data on attacker damage potential, and defender base stats, 
# to generate convex optimization datasets based on Pokemon data. 
#
###############################################################################################

#Pokemon Constants
HP =  0
ATK = 1
DEF = 2
SPA = 3
SPD = 4
SPE = 5

UPNATURES = {
    HP: [], 
    ATK: ["Adamant", "Brave", "Lonely", "Naughty"], 
    DEF: [],
    SPA: ["Modest", "Quiet", "Mild", "Rash"],
    SPD: [],
    SPE: []
}

DOWNNATURES = {
    HP: [], 
    ATK: ["Modest", "Timid", "Bold", "Calm"], 
    DEF: [],
    SPA: ["Adamant", "Jolly", "Impish", "Careful"],
    SPD: [],
    SPE: []
}

####################################################
# Calculating beta values for a given problem
####################################################

# Continuous, simplified approximator for damage formula 
#   (from attacker side, not defender - defender handled by an optimizer)
# currently, calcs for STAB base 100 move (Pokemon note - this is roughly post-tera tera blast for pre-existing STAB)
def calcDamage(stat, base_power=100):
    return base_power*stat*2/5*1.5

#takes base_stats as an array of 3 ints representing base stats for HP, Def, SpD, and calculates Beta Values
def calc_betas(base_stats = [80, 80, 80], base_atk=100, base_pow=100, base_special_attack=100, base_special_pow = 100, spread="Serious:0/0/0/0/0/0"): 
    b2 = base_stats[0] + 75 + 32
    b3 = base_stats[1] + 20 + 32
    b4 = base_stats[2] + 20 + 32
    b1 = calcDamage(calcStat(base_atk, spread, ATK), base_pow)
    b5 = calcDamage(calcStat(base_special_attack, spread, ATK), base_special_pow)

    return [b1, b2, b3, b4, b5]



def calcStat(base, spread, stat=ATK):
    nature = spread[0:spread.index(":")]
    iv = 31 #assume maximum IV - conservative for optimizing defensive spreads. 
    speedEvs = int(spread.split('/')[stat])
    if nature in UPNATURES[stat]:
        multiplier = 1.1
    else:
        if nature in DOWNNATURES[stat]:
            multiplier = .9
        else: 
            multiplier = 1
    stat = math.floor(math.floor(base + 5 + iv/2 + speedEvs/8)*multiplier)
    return stat

#########################################
# Build problems from Pokemon Datasets
#########################################


ATTACKER = 'charizard'
ATTACK_STATS = [84, 109] #todo - fetch this from an old pokedex api, like for eggsteps project (https://pokeapi.co/ , can query pokemon/[attacker name] and look at "stats" with certain indices)
ATTACK_POWS = [120, 150] #not sure best way to grab this - may default to 100s for now. Can query pokeapi with move/[move-name] to get base power, physical/special and check for type

DEFENDER = 'raichu'
DEFENDER_STATS = [60, 55, 80]

print(calc_betas(DEFENDER_STATS, ATTACK_STATS[0], ATTACK_POWS[0], ATTACK_STATS[1], ATTACK_POWS[1], spread='Serious:0/252/0/252/0/0'))

# Can get usage rates for spreads on attacker, pokemon doing the attacking, maybe base power of attack moves (will need to integrate with API)

# DATASET = "https://www.smogon.com/stats/2020-04/chaos/gen8vgc2020-0.json"
# data = json.loads(urlopen(DATASET).read())

# spreadObjects = data["data"][ATTACKER]["Spreads"]


#note - could use damage calc API to get exact damage formulas

###################
### Archived Code
##################

# old code used to generate CDF for speed stats of a given Pokemon - can be repurposed for attack stats, and damage thresholds. 

# def calcSpeeds(baseSpeed, spreadObjects):
#     maxSpeed = calcSpeed(baseSpeed, "Jolly:0/0/0/0/0/252")
#     minSpeed = calcSpeed(baseSpeed, "Quiet:0/0/0/0/0/0")
#     speedCounts = np.zeros(maxSpeed - minSpeed + 1)
#     spreads = list(spreadObjects.keys())
#     counts = list(spreadObjects.values())
#     for j in range(len(spreadObjects)):
#         speed = calcSpeed(baseSpeed, spreads[j])
#         speedCounts[speed - minSpeed] += counts[j]
#     #for i in range(len(speedCounts)):
#     #    print("Speed "+str(i + minSpeed) + ": " + str(speedCounts[i]))
#     return speedCounts, minSpeed