import random

from universal_automl.automl_systems_info import automl_systems_info


def get_automl_system_info() -> dict:
    """
    Get random automl system info

    Get randomly selected automl system info from our automl systems info dict

    :return: selected automl
    :rtype: dict
    """
    return automl_systems_info[random.randint(0, len(automl_systems_info) - 1)]
