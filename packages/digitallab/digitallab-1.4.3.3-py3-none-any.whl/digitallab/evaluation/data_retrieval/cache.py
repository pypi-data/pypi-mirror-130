#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#
import json
import os
import warnings
from typing import Union

import pandas as pd
import hashlib


class Cache:
    def __init__(self, experiment_name, experiment_version, last_changed, keys: dict, id: Union[str, None] = None,
                 dir="/tmp/", force_loading_cache=False):
        assert isinstance(keys, dict)
        self._mongo_last_changed = last_changed
        self.dir = dir
        self.id = id if id is not None else experiment_name
        self.experiment_name = experiment_name
        self.experiment_version = experiment_version
        self._keys_hash = hashlib.sha512(str(keys).encode("utf-8")).hexdigest()
        self.cache = None
        self.load_cache(force_loading_cache)

    def load_cache(self, force_loading_cache):
        if os.path.isfile(self.dir + "/" + self.get_cache_hash_file_name()) and os.path.isfile(
                self.dir + "/" + self.get_cache_file_name()):
            if force_loading_cache:
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore", category=DeprecationWarning)
                    self.cache = pd.read_hdf(self.dir + "/" + self.get_cache_file_name(), "table")
            else:
                with open(self.dir + "/" + self.get_cache_hash_file_name(), "rb") as cache_hash:
                    hashes = json.load(cache_hash)
                if self.cache_hit(hashes):
                    with warnings.catch_warnings():
                        warnings.filterwarnings("ignore", category=DeprecationWarning)
                        self.cache = pd.read_hdf(self.dir + "/" + self.get_cache_file_name(), "table")
                else:
                    print("No cache hit. Rebuilding data.")
        else:
            print("Cache not found. Creating new cache.")

    def cache_hit(self, hashes: dict):
        hit = True
        hit &= hashes["last_changed"] == str(self._mongo_last_changed)
        hit &= hashes["experiment"] == self.experiment_name
        hit &= hashes["version"] == self.experiment_version
        hit &= hashes["keys_hash"] == self._keys_hash
        return hit

    def get_cache_file_name(self):
        return "cache_" + self.id + "_" + self.experiment_version + ".h5"

    def get_cache_hash_file_name(self):
        return "cache_hash_" + self.id + "_" + self.experiment_version + ".json"

    def save_cache(self, data):
        self.cache = data
        with open(self.dir + "/" + self.get_cache_hash_file_name(), "w") as cache_hash:
            d = {"experiment": self.experiment_name,
                 "version": self.experiment_version,
                 "last_changed": str(self._mongo_last_changed),
                 "keys_hash": self._keys_hash}
            json.dump(d, cache_hash)
        data.to_hdf(self.dir + "/" + self.get_cache_file_name(), "table", append=False)

    def clear_cache(self):
        if os.path.isfile(self.dir + "/" + self.get_cache_hash_file_name()):
            os.remove(self.dir + "/" + self.get_cache_hash_file_name())
            print("Removed " + self.dir + "/" + self.get_cache_hash_file_name())
        else:
            print("The file " + self.dir + "/" + self.get_cache_hash_file_name() +
                  " could not be found and hence was not removed.")
        if os.path.isfile(self.dir + "/" + self.get_cache_file_name()):
            os.remove(self.dir + "/" + self.get_cache_file_name())
            print("Removed " + self.dir + "/" + self.get_cache_file_name())
        else:
            print("The file " + self.dir + "/" + self.get_cache_file_name() +
                  " could not be found and hence was not removed.")
