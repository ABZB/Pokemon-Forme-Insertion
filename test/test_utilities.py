import unittest

from utilities import max_of_column, entire_of_column


class TestUtilities(unittest.TestCase):
    def test_max_of_column(self):
        example_table = [
            [
                1, "a", 2
            ],
            [
                3, 4, "b"
            ]
        ]

        self.assertEqual(max_of_column(example_table, 0), 3)
        self.assertEqual(max_of_column(example_table, 1), 4)
        self.assertEqual(max_of_column(example_table, 2), 2)

    def test_entire_of_column(self):
        example_table = [
            [
                1, "a", 2
            ],
            [
                3, 4, "b"
            ]
        ]
        self.assertEqual(entire_of_column(example_table, 0, allow_multiple=False), [1, 3])
        self.assertEqual(entire_of_column(example_table, 1, allow_multiple=False), ["a", 4])
        self.assertEqual(entire_of_column(example_table, 2, allow_multiple=False), [2, "b"])


if __name__ == '__main__':
    unittest.main()
