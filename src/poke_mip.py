from docplex.mp.model import Model

def build(b):
    assert len(b) == 5

    m = Model(name='pokemon_QCP')

    # by default they have a lower bound of 0 and an infinite upper bound
    x1 = m.integer_var(name='x1')
    x2 = m.integer_var(name='x2')
    x3 = m.integer_var(name='x3')

    # (b1/x2) - x1 <= .0001
    # -x1x2 <= -b1 + .0001
    m.add(-x1 * x2 <= -b[0] + .0001)

    # x1 <= b1
    m.add_constraint(x1 <= b[0])

    # x2 <= b2
    m.add_constraint(x2 <= b[1])

    # x3 <= b3
    m.add_constraint(x3 <= b[2])

    # x1 >= b1 - 32
    m.add_constraint(x1 >= b[0] - 32)

    # x2 >= b2 - 32
    m.add_constraint(x2 >= b[1] - 32)

    # x3 >= b3 - 32
    m.add_constraint(x3 >= b[2] - 32)

    # (b4 / x2) - x1 <= .0001
    # -x1x2 <= -b4 + .0001
    m.add(-x1 * x2 <= -b[3] + .0001)

    # (b5 / x3) - x1 <= .0001
    # -x1x3 <= -b5 + .0001
    m.add(-x1 * x3 <= -b[4] + .0001)

    m.minimize(x1 + x2 + x3)

    return m
