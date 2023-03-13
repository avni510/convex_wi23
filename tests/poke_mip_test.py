import unittest
from src import poke_mip

class TestMIP(unittest.TestCase):
    def test_simple_case(self):
        b = [167, 107, 132, 9792, 24150]

        m = poke_mip.build(b)
        m.print_information()
        m.solve(log_output=True)
        m.print_solution()




