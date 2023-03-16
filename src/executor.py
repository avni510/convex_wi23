from src import poke_mip
import numpy as np

def run(dataset):
    """
    :param dataset numpy array
    :return an array of dictionaries containing info of the solved optimization problem
    """

    U = np.unique(dataset, axis = 0)

    results = []
    for b in U:
        info = {
                "is_infeasible": None,
                "objective_val": None,
                "x": [],
                "b": b
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
