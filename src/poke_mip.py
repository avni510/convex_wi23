from docplex.mp.model import Model

def build(b):
    assert len(b) == 5

    m = Model(name='pokemon_QCP')

    # by default they have a lower bound of 0 and an infinite upper bound
    x1 = m.integer_var(name='x1')
    x2 = m.integer_var(name='x2')
    x3 = m.integer_var(name='x3')

    # (b1/x2) - x1 < 0
    # -x1x2 <= -b1 + .0001
    m.add(-x1 * x2 <= -b[0] + .0001)

    # x1 <= b1
    m.add_constraint(x1 <= b[0])

    # x2 <= b2
    m.add_constraint(x2 <= b[1])

    # x3 <= b3
    m.add_constraint(x3 <= b[2])

    # (b4 / x2) - x1 < 0
    # -x1x2 <= -b4 + .0001
    m.add(-x1 * x2 <= -b[3] + .0001)

    # (b5 / x3) - x1 < 0
    # -x1x3 <= -b5 + .0001
    m.add(-x1 * x3 <= -b[4] + .0001)

    m.minimize(x1 + x2 + x3)

    return m

# def build(b):
#     assert len(b) == 5
#
#     mip = cplex.Cplex()
#     # mip.set_problem_type(mip.problem_type.MILP)
#
#     var = mip.variables
#     lin_cons = mip.linear_constraints
#     quad_cons = mip.quadratic_constraints
#
#     mip.objective.set_sense(mip.objective.sense.minimize)
#
#     x = [f'x[{i}]' for i in range(1, 4)]
#
#     indices = {
#             'obj': [1.0] * len(x),
#             'names': {'x': x},
#             'types': {'x': "CCC"},
#             'lb': {'x': [0.0, 0.0, 0.0]},
#             'ub': {'x': [1e10, 1e10, 1e10]},
#             'params': {'b': b}
#             }
#
#     concatenate_values = lambda d: list(chain.from_iterable(d.values()))
#     var.add(
#             obj = indices['obj'],
#             names = concatenate_values(indices['names']),
#             types = concatenate_values(indices['types']),
#             lb = concatenate_values(indices['lb']),
#             ub = concatenate_values(indices['ub'])
#             )
#
#     quad_cons.add(
#         name='b1_x2_x1',
#         quad_expr=cplex.SparseTriple(
#             ind1 = ['x[1]'],
#             ind2 = ['x[2]'],
#             val = [-1.0]
#             ),
#         sense="L",
#         rhs=indices['params']['b'][0] * -1 + 1
#         )
#
#     # x1 <= b1
#     lin_cons.add(
#         names=['x1_b1'],
#         lin_expr=[cplex.SparsePair(
#             ind= [indices['names']['x'][0]],
#             val= [1.0]
#             )],
#         senses="L",
#         rhs=[indices['params']['b'][0]]
#         )
#
#     # x2 <= b2
#     lin_cons.add(
#         names=['x2_b2'],
#         lin_expr=[cplex.SparsePair(
#             ind= [indices['names']['x'][1]],
#             val= [1.0]
#             )],
#         senses="L",
#         rhs=[indices['params']['b'][1]]
#         )
#
#     # x3 <= b3
#     lin_cons.add(
#         names=['x3_b3'],
#         lin_expr=[cplex.SparsePair(
#             ind= [indices['names']['x'][2]],
#             val= [1.0]
#             )],
#         senses="L",
#         rhs=[indices['params']['b'][2]]
#         )
#
#     # (b4 / x2) - x1 < 0
#     # -x1x2 <= -b4 + 1
#     quad_cons.add(
#         name='b4_x2_x1',
#         quad_expr=cplex.SparseTriple(
#             ind1= ['x[1]'],
#             ind2= ['x[2]'],
#             val= [-1.0]
#             ),
#         sense="L",
#         rhs=indices['params']['b'][3] * -1 + 1
#         )
#
#
#     # (b5 / x3) - x1 < 0
#     # -x1x3 <= -b5 + 1
#     quad_cons.add(
#         name='b5_x2_x1',
#         quad_expr=cplex.SparseTriple(
#             ind1= ['x[1]'],
#             ind2= ['x[3]'],
#             val= [-1.0]
#             ),
#         sense="L",
#         rhs=indices['params']['b'][4] * -1 + 1
#         )
#
#     return mip, indices
