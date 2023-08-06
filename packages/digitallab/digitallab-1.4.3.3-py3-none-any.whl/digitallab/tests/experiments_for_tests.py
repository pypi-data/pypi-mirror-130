import numpy as np

standard_setting = {
    "experiment": "test",
    "sub_experiment": "standard",
    "version": "1",
    "number_of_repetitions": 10,
    "method": ["slow", "fast"],
    "instance": ["A", "B"]
}

error_setting = {
    "experiment": "test",
    "sub_experiment": "standard",
    "version": "1",
    "number_of_repetitions": 10,
    "method": ["slow", "fast"],
    "instance": ["A", "C"]
}

special_setting = {
    "experiment": "test",
    "sub_experiment": "special",
    "version": "1",
    "number_of_repetitions": 10,
    "method": "special",
    "scale": [0.1, 0.5, 1],
    "instance": ["A", "B"]
}


def slow(config):
    np.random.seed(config["seed"])
    return_dict = dict()
    if config["instance"] == "A":
        return_dict["runtime"] = np.max(np.random.normal(1000, scale=300), 0)
        return_dict["value"] = np.random.normal(1, scale=0.5)
    elif config["instance"] == "B":
        return_dict["runtime"] = np.max(np.random.normal(10000, scale=300), 0)
        return_dict["value"] = np.random.normal(10, scale=0.5)
    else:
        raise RuntimeError("Test error.")
    return return_dict


def fast(config):
    np.random.seed(config["seed"])
    return_dict = dict()
    if config["instance"] == "A":
        return_dict["runtime"] = np.max(np.random.normal(200, scale=100), 0)
        return_dict["value"] = np.random.normal(2, scale=0.7)
    else:
        return_dict["runtime"] = np.max(np.random.normal(2000, scale=100), 0)
        return_dict["value"] = np.random.normal(20, scale=0.7)
    return return_dict


def special(config):
    np.random.seed(config["seed"])
    return_dict = dict()
    if config["instance"] == "A":
        return_dict["runtime"] = np.max(np.random.normal(500, scale=100), 0)
        return_dict["value"] = np.random.normal(1.5, scale=config["scale"])
    else:
        return_dict["runtime"] = np.max(np.random.normal(5000, scale=100), 0)
        return_dict["value"] = np.random.normal(15, scale=config["scale"])
    return return_dict
