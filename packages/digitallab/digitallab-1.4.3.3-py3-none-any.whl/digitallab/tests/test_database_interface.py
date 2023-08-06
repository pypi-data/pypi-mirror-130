from unittest import TestCase

from digitallab.helper.database_interface import remove_tree_depth


class Test(TestCase):
    def test_remove_tree_depth(self):
        d = {"config": {"version": "test", "number_of_repetitions": 10}}
        depthless_dictonary = remove_tree_depth(d)
        self.assertIn("config.version", depthless_dictonary.keys())
        self.assertEqual(depthless_dictonary["config.version"], "test")
        self.assertIn("config.number_of_repetitions", depthless_dictonary.keys())
        self.assertEqual(depthless_dictonary["config.number_of_repetitions"], 10)
