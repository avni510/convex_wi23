import math
import numpy as np
import json
from urllib.request import urlopen
import requests
import pandas as pd

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
def calc_betas(base_stats = [80, 80, 80], base_offense = [100, 100], base_pows=[100, 100], spread="Serious:0/252/0/252/0/0"): 
    b2 = base_stats[0] + 75 + 32
    b3 = base_stats[1] + 20 + 32
    b4 = base_stats[2] + 20 + 32
    b1 = calcDamage(calcStat(base_offense[0], spread, ATK), base_pows[0])
    b5 = calcDamage(calcStat(base_offense[1], spread, SPA), base_pows[1])

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

# print(calc_betas(DEFENDER_STATS, ATTACK_STATS[0], ATTACK_POWS[0], ATTACK_STATS[1], ATTACK_POWS[1], spread='Serious:0/252/0/252/0/0'))


# takes a pokemon species name as a lower case string
# returns array of [attack base stat, special attack base stat]
def get_attack_stats(pokemon): 
    response = requests.get('https://pokeapi.co/api/v2/pokemon/'+pokemon)
    if not response.ok:
        print("error with json request for Pokemon " + pokemon)
        return -1
    else: 
        data = json.loads(response.content)
        return [data['stats'][ATK]['base_stat'], data['stats'][SPA]['base_stat']]

# returns array of defense stats
def get_defense_stats(pokemon): 
    response = requests.get('https://pokeapi.co/api/v2/pokemon/'+pokemon)
    if not response.ok:
        print("error with json request for Pokemon " + pokemon)
        return -1
    else: 
        data = json.loads(response.content)
        return [data['stats'][HP]['base_stat'], data['stats'][DEF]['base_stat'], data['stats'][SPD]['base_stat']]

# print(get_attack_stats('charizard'))

# takes pokemon species name as lower case string
# returns highest base power physical and special moves of the Pokemon's type
def get_attack_pows(pokemon): 
    # return [150, 150] #stub
    max_pows = [0, 0]
    response = requests.get('https://pokeapi.co/api/v2/pokemon/'+pokemon)
    if not response.ok:
        print("error with json request for Pokemon " + pokemon)
        return -1
    else: 
        data = json.loads(response.content)

        pkmn_types = [] #track types of the pokemon
        json_for_pkmn_types = data['types']
        for pkmn_type in json_for_pkmn_types: 
            pkmn_types.append(pkmn_type['type']['name'])

        moves = data['moves']
        for move in moves:
            response = requests.get(move['move']['url'])
            if not response.ok:
                print("error with json request for move " + str(move))
                return -1
            else: 
                move_data = json.loads(response.content)
                if move_data['type']['name'] in pkmn_types:
                    if move_data['damage_class']['name'] == 'physical': 
                        if move_data['power'] and (max_pows[0] < move_data['power']): 
                            max_pows[0] = move_data['power']
                    elif move_data['damage_class']['name'] == 'special': 
                        if move_data['power'] and (max_pows[1] < move_data['power']): 
                            max_pows[1] = move_data['power']
        
        return max_pows

# print(get_attack_pows('charizard'))

#################################
### generate first dataset
#################################

attackers = ['charizard', 'snorlax']
defenders = ['snorlax', 'raichu']

df = pd.DataFrame(columns=['b1', 'b2', 'b3', 'b4', 'b5', 'attacker', 'defender'])

for attacker in attackers: 
    for defender in defenders: 
        betas = calc_betas(get_defense_stats(defender), get_attack_stats(attacker), get_attack_pows(attacker)) #uses default argument for spread for now
        df.loc[df.shape[0]] = betas + [attacker, defender]

df.to_csv('dataset-draft-1.csv', index=False)
        

    
# #takes move json
# def check_move(url, type, category='physical')

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