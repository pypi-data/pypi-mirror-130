from unittest import TestCase

from digitallab.helper.generate_seeds import generate_seeds


class TestSeeds(TestCase):
    def test_different_number_of_seeds_generate_same_seeds(self):
        seeds1 = generate_seeds(10)
        seeds2 = generate_seeds(20)
        for i in range(10):
            self.assertEqual(seeds1[i], seeds2[i])
