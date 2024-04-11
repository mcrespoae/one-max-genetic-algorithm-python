import unittest
from one_max_genetic_algorithm_python.utils import generate_equally_spaced_values


class TestGenerateEquallySpacedValues(unittest.TestCase):
    def test_default_values(self):
        # Test with default parameters
        expected_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        self.assertEqual(generate_equally_spaced_values(), expected_values)

    def test_custom_values(self):
        # Test with custom parameters
        min_val = 2.0
        max_val = 5.0
        length = 4
        expected_values = [2.0, 3.0, 4.0, 5.0]
        self.assertEqual(generate_equally_spaced_values(min_val, max_val, length), expected_values)

    def test_edge_case_length_1(self):
        # Test when length is 1
        expected_values = [0.1]
        self.assertEqual(generate_equally_spaced_values(length=1), expected_values)

    def test_edge_case_same_values(self):
        # Test when min_val and max_val are the same
        min_val = 3.0
        max_val = 3.0
        length = 5
        expected_values = [3.0, 3.0, 3.0, 3.0, 3.0]
        self.assertEqual(generate_equally_spaced_values(min_val, max_val, length), expected_values)

    def test_invert_parameter(self):
        # Test with invert parameter set to True
        min_val = 2.0
        max_val = 5.0
        length = 4
        expected_values = [5.0, 4.0, 3.0, 2.0]
        self.assertEqual(generate_equally_spaced_values(min_val, max_val, length, invert=True), expected_values)

if __name__ == '__main__':
    unittest.main()