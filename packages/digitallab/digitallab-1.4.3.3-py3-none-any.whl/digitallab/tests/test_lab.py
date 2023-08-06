import os
import shutil
from unittest import TestCase

from digitallab.lab import Lab
from digitallab.tests.experiments_for_tests import *

lab = Lab("Test").add_tinydb_storage("test_tiny")


@lab.experiment
def main(_config):
    if _config["method"] == "fast":
        return fast(_config)
    elif _config["method"] == "slow":
        return slow(_config)
    elif _config["method"] == "special":
        return special(_config)


class TestLab(TestCase):
    def setUp(self) -> None:
        if os.path.isdir("test_tiny"):
            shutil.rmtree("test_tiny")

    def test_experiments_run_without_error(self):
        lab.run_experiments(main, standard_setting, number_of_query_chunks=100, number_of_parallel_runs=1,
                            number_of_query_workers=1)

    def test_multiple_experiments_run_without_error(self):
        lab.run_experiments(main, [standard_setting, special_setting], number_of_query_chunks=100,
                            number_of_parallel_runs=1, number_of_query_workers=1)

    def test_lab_catches_errors(self):
        lab.run_experiments(main, error_setting, number_of_query_chunks=100, number_of_parallel_runs=1,
                            number_of_query_workers=1)
        self.assertEqual(lab.get_recent_number_of_failed_instances(), 10)

    def test_logging_does_not_throw_an_error(self):
        lab.run_experiments(main, error_setting, number_of_query_chunks=100, number_of_parallel_runs=1,
                            number_of_query_workers=1, path_to_log="test.log")
