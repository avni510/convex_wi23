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

#########################
### Pokemon Constants ###
#########################
HP = 0
ATK = 1
DEF = 2
SPA = 3
SPD = 4
SPE = 5

UPNATURES = {
    HP: [],
    ATK: ['Boost-Offense', "Adamant", "Brave", "Lonely", "Naughty"],
    # introduced fake nature, 'Boost-Offense', which boosts attack and special attack, so that we can get upper bounds on an attacking Pokemon, whether its nature boosts attack or special attack
    DEF: [],
    SPA: ['Boost-Offense', "Modest", "Quiet", "Mild", "Rash"],
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
# adds 4/3 boost for tera
def calcDamage(stat, base_power=100, tera=True):
    return base_power * stat * 2 / 5 * 1.5 * (4 / 3 if tera else 1)


# takes base_stats as an array of 3 ints representing base stats for HP, Def, SpD, and calculates Beta Values
def calc_betas(base_stats=[80, 80, 80], base_offense=[100, 100], base_pows=[100, 100],
               spread="Boost-Offense:0/252/0/252/0/0"):
    b1 = base_stats[0] + 75 + 32
    b2 = base_stats[1] + 20 + 32
    b3 = base_stats[2] + 20 + 32
    b4 = calcDamage(calcStat(base_offense[0], spread, ATK), base_pows[0])
    b5 = calcDamage(calcStat(base_offense[1], spread, SPA), base_pows[1])

    return [b1, b2, b3, b4, b5]


def calcStat(base, spread, stat=ATK):
    nature = spread[0:spread.index(":")]
    iv = 31  # assume maximum IV - conservative for optimizing defensive spreads.
    speedEvs = int(spread.split('/')[stat])
    if nature in UPNATURES[stat]:
        multiplier = 1.1
    else:
        if nature in DOWNNATURES[stat]:
            multiplier = .9
        else:
            multiplier = 1
    stat = math.floor(math.floor(base + 5 + iv / 2 + speedEvs / 8) * multiplier)
    return stat


#########################################
# Build problems from Pokemon Datasets
#########################################

# takes a pokemon species name as a lower case string
# returns array of [attack base stat, special attack base stat]
def get_attack_stats(pokemon):
    response = requests.get('https://pokeapi.co/api/v2/pokemon/' + pokemon)
    if not response.ok:
        print("error with json request for Pokemon " + pokemon)
        return -1
    else:
        data = json.loads(response.content)
        return [data['stats'][ATK]['base_stat'], data['stats'][SPA]['base_stat']]


# returns array of defense stats
def get_defense_stats(pokemon):
    response = requests.get('https://pokeapi.co/api/v2/pokemon/' + pokemon)
    if not response.ok:
        print("error with json request for Pokemon " + pokemon)
        return -1
    else:
        data = json.loads(response.content)
        return [data['stats'][HP]['base_stat'], data['stats'][DEF]['base_stat'], data['stats'][SPD]['base_stat']]


# takes pokemon species name as lower case string
# returns highest base power physical and special moves of the Pokemon's type
def get_attack_pows(pokemon):
    # return [150, 150] #stub
    max_pows = [0, 0]
    response = requests.get('https://pokeapi.co/api/v2/pokemon/' + pokemon)
    if not response.ok:
        print("error with json request for Pokemon " + pokemon)
        return -1
    else:
        data = json.loads(response.content)

        pkmn_types = []  # track types of the pokemon
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


#################################
### generate first dataset
#################################

attackers = ['bulbasaur', 'charmander', 'squirtle', 'pikachu', 'ninetales', 'jigglypuff', 'diglett', 'psyduck', 'abra',
             'onix', 'drowzee']
# ['flutter-mane', 'iron-bundle', 'iron-hands', 'great-tusk', 'gholdengo',
# 'amoonguss', 'arcanine', 'dondozo', 'tatsugiri', 'dragonite', 'roaring-moon',
# 'kingambit']
# , 'maushold', 'brute-bonnet', 'talonflame', 'armarouge', 'indeedee-female', 
# 'torkoal', 'tyranitar', 'palafin-hero', 'annihilape', 'iron-moth', 'sylveon', 
# 'garganacl', 'murkrow', 'volcarona', 'gothitelle', 'mimikyu', 'baxcalibur', 
# 'glimmora', 'hatterene', 'pelipper', 'grimmsnarl', 'garchomp', 
# 'ceruledge', 'scream-tail', 'meowscarada', 'gastrodon', 'sandy-shocks', 
# 'oranguru', 'farigiraf', 'rotom-wash', 'hariyama', 'iron-jugulis', 
# 'corviknight', 'lycanroc', 'abomasnow', 'pawmot', 'salamence', 'scizor', 
# 'sableye', 'espathra', 'hydreigon', 'gyarados', 'tauros-paldea-aqua']
defenders = attackers  # use same list for now

df = pd.DataFrame(columns=['b1', 'b2', 'b3', 'b4', 'b5', 'attacker', 'defender'])

defense_stats = {}
attack_stats = {}
attack_pows = {}
## queries to API:
progress = 0
total_to_calc = len(attackers)
for attacker in attackers:
    attack_stats[attacker] = get_attack_stats(attacker)
    attack_pows[attacker] = get_attack_pows(attacker)
    progress += 1
    print('progress: ' + str(progress) + ' / ' + str(total_to_calc))

progress = 0
total_to_calc = len(defenders)
for defender in defenders:
    defense_stats[defender] = get_defense_stats(defender)
    progress += 1
    print('progress: ' + str(progress) + ' / ' + str(total_to_calc))

for attacker in attackers:
    for defender in defenders:
        betas = calc_betas(defense_stats[defender], attack_stats[attacker],
                           attack_pows[attacker])  # uses default argument for spread for now
        df.loc[df.shape[0]] = betas + [attacker, defender]

from datetime import datetime

date_time = datetime.now().strftime("%m_%d_%H_%M_%S")
save_file = f'dataset_{date_time}.csv'
df.to_csv(save_file, index=False)
print('dataset saved to : ', save_file)
