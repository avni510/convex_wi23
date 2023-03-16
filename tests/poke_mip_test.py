import unittest
import warnings
warnings.filterwarnings("ignore")
from src import poke_mip

class TestMIP(unittest.TestCase):
    def test_simple_case(self):
        b = [167, 107, 132, 9792, 14490]

        m = poke_mip.build(b)
        m.print_information()
        m.solve()

        self.assertEqual(m.objective_value, 318)
        self.assertEqual(m.solution.get_value('x1'), 135)
        self.assertEqual(m.solution.get_value('x2'), 75)
        self.assertEqual(m.solution.get_value('x3'), 108)
