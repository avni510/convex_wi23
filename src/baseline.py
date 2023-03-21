import numpy as np


# based on https://www.vgcguide.com/eving-1-how-to-make-simple-ev-spreads
# considers a small set of candidate spreads. We compare 
# 
# "Go straight to HP and the defenses. Pick a defensive stat to put EVs in based on that Pokémon’s stats, and put EVs into Defense or Special Defense accordingly. 
#  Split evenly or evenly-ish if you can’t decide.."

#note that this is a fair baseline for an automated tool, because other ones require expertise, world champ level
def check_constraints(b, x):
    for i in [0, 1, 2]: 
        if (b[i] < x[i]) or (x[i] < b[i] - 32): 
            return False
    
    if b[3]/x[1] - x[0] > 0:
        return False
    
    if b[4]/x[2] - x[0] > 0: 
        return False
    
    return True



def build(b):
    b1, b2, b3, b4, b5 = b


    possible_solutions = [[b1-32, b2-32, b3-32], [b1, b2-32, b3-32], [b1, b2, b3-32], [b1, b2-32, b3], [b1, b2-16, b3-16], [b1, b2, b3]] #technically, the last option is not feasible in game; anything with minimal objective exceeding b1 + b2 + b3 - 32 is in this boat. That said, we can just calculate this way and note if no feasible option exists 

    for solution in possible_solutions: 
        if check_constraints(b, solution): 
            return sum(solution), solution[0], solution[1], solution[2]
    # print('infeasible')
    return -1, -1, -1, -1
        