from src import poke_mip
import numpy as np

def run(bs, attackers, defenders):
    """
    :param bs numpy array
    :param attackers numpy array
    :param defenders numpy array
    :return an array of dictionaries containing info of the solved optimization problem
    """
    assert len(bs) == len(attackers) == len(defenders)

    results = []
    for b, attacker, defender in zip(bs, attackers, defenders):
        info = {
                "is_infeasible": None,
                "objective_val": None,
                "x": [],
                "b": b,
                "attacker": attacker,
                "defender": defender,
                }

        m = poke_mip.build(b)

        m.solve()
        if "infeasible" in m.solve_details.status:
            info["is_infeasible"] = True
            results.append(info)
        else:
            info["is_infeasible"] = False
            info["objective_val"] = m.objective_value
            info["x"] = [
                    m.solution.get_value('x1'),
                    m.solution.get_value('x2'),
                    m.solution.get_value('x3')
                    ]
            results.append(info)
    return results
