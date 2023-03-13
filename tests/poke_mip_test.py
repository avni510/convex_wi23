import unittest
from src import poke_mip
import cplex

class TestMIP(unittest.TestCase):
    def test_simple_case(self):
        b = [167, 107, 132, 9792, 24150]

        mip, indices = poke_mip.build(b)

        import pdb; pdb.set_trace()
        mip.solve()

        x_indices = indices['names']['x']
        x_values = mip.solution.get_values(x_indices)
        print(x_values)
        self.assertEqual(x_values, [145, 75, 110])



