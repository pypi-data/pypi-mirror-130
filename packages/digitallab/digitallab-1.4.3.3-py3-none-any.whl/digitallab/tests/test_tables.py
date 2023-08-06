import os
from unittest import TestCase

from digitallab.lab import Lab
from digitallab.tests.experiments_for_tests import *

lab = Lab("test").add_tinydb_storage("test_tiny")


@lab.experiment
def main(_config):
    if _config["method"] == "fast":
        return fast(_config)
    elif _config["method"] == "slow":
        return slow(_config)
    elif _config["method"] == "special":
        return special(_config)


class TestTables(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not os.path.isdir("test_tiny"):
            lab.run_experiments(main, [standard_setting, special_setting], number_of_query_chunks=100,
                                number_of_parallel_runs=1, number_of_query_workers=1)

    def test_table_builds_without_errors(self):
        table = lab.mean_table("1"). \
            set_methods_key("method", label="Method"). \
            add_unit_to_compare("Fast", method="fast"). \
            add_unit_to_compare("Slow", method="slow"). \
            add_unit_to_compare("Special", method="special"). \
            set_value_of_interest("runtime"). \
            set_instance_keys(["instance"], labels=["Instance"]). \
            build_table()
        print(table)
