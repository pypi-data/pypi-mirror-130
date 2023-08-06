#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import json
import random
from typing import Union

from digitallab.helper.experiment_setting import ExperimentCollection


def generate_seeds(number_of_repetitions, master_seed=42):
    random.seed(master_seed)
    return random.sample(range(int(1e8)), k=number_of_repetitions)


def generate_seeds_from_json_or_dict(json_path_or_dict: Union[str, dict], master_seed=42):
    if isinstance(json_path_or_dict, str):
        with open(json_path_or_dict) as json_file:
            setting = json.load(json_file)
    elif isinstance(json_path_or_dict, dict):
        setting = json_path_or_dict
    else:
        raise ValueError("'json_path_or_dict' must be a dictionary or a string.")

    return generate_seeds(setting["number_of_repetitions"], master_seed=master_seed)


def generate_seeds_from_experiment_collection(experiment_collection: ExperimentCollection, master_seed=42):
    max_number_of_repetitions = max(
        [experiment_setting.setting["number_of_repetitions"] for experiment_setting in experiment_collection])
    return generate_seeds(max_number_of_repetitions, master_seed=master_seed)
