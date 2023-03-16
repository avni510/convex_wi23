import unittest
import warnings
import numpy as np
warnings.filterwarnings("ignore")
from src import executor

class TestExecutor(unittest.TestCase):
    def test_two_values(self):
        b_1 = [167, 107, 132, 9792, 14490]
        b_2 = [167, 107, 132, 9792, 24000]
        dataset = np.array([b_1, b_2])

        results = executor.run(dataset)

        self.assertEqual(len(results), 2)

        info_1 = results[0]

        self.assertEqual(info_1["is_infeasible"], False)
        self.assertEqual(info_1["objective_val"], 318)
        self.assertTrue(np.array_equal(info_1["x"], [135, 75, 108]))
        self.assertTrue(np.array_equal(info_1["b"], b_1))

        info_2 = results[1]

        self.assertEqual(info_2["is_infeasible"], True)
        self.assertEqual(info_2["objective_val"], None)
        self.assertTrue(np.array_equal(info_2["x"], []))
        self.assertTrue(np.array_equal(info_2["b"], b_2))
