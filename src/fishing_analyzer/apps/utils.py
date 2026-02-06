from typing import Any, Dict, List

from fishing_analyzer import config, utils


def generate_attribute_options(fish_model: Any) -> list[dict[str, str]]:
    """Generiert Optionen für Dropdown-Menüs basierend auf plotbaren Attributen.

    Args:
        fish_model: Das Fischmodell, das die plotbaren Attribute enthält.

    Returns:
        Eine Liste von Dictionaries, die "label" und "value" für jedes Attribut enthalten.
    """
    return_list: list[dict[str, str]] = list()

    for attribute in fish_model.plotable_attributes:
        name: str = utils.attribute_to_name(attribute)
        return_list.append({"label": name, "value": attribute})

    return return_list


def generate_fish_type_options(fish_model: Any) -> list[dict[str, str]]:
    return_list: list[dict[str, str]] = list()

    for fish_type in config.FISH_TYPES:
        fish_frame: Any = fish_model.get_fish_frame(fish_type)

        if utils.is_valid_fish_frame(fish_frame):
            return_list.append({"label": fish_type, "value": fish_type})

    return return_list


def generate_year_options() -> list[dict[str, str]]:
    return_list: list[dict[str, str]] = list()

    for year in config.YEAR_RANGE:
        return_list.append({"label": year, "value": year})

    return return_list


def generate_month_options() -> list[dict[str, str]]:
    return_list: list[dict[str, str]] = list()

    for month_index, month_name in config.MONTH_NAME_DICT.items():
        return_list.append({"label": month_name.title(), "value": month_index})

    return return_list


def generate_day_options() -> list[dict[str, str]]:
    return_list: list[dict[str, str]] = list()

    for day_index, day_value in config.MONTH_DAYS_DICT.items():
        return_list.append({"label": str(day_index), "value": str(day_index)})

    return return_list


def generate_method_options() -> list[dict[str, str]]:
    return_list: list[dict[str, str]] = list()

    for method in config.STATISTIC_METHODS:
        return_list.append({"label": method.title(), "value": method})

    return return_list
