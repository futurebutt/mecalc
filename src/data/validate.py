import json
import string
from typing import Any

from venums import *


TALENT_RANKS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
TALENT_DATA_TYPES = [
    NAME := "name",
    ROOT := "root",
    PERCENT_BONUS := "percent_bonus",
    ABSOLUTE_BONUS := "absolute_bonus",
    SPECIALIZATION := "specialization"
]
MIN_NAME_LEN = 1
MAX_NAME_LEN = 16


def is_talent_file_valid(filename: str) -> bool:

    with open(filename, "r") as f:
        talent_data: dict = json.load(f)

    valid = is_talent_data_valid(talent_data)
    return valid


def is_talent_data_valid(talent_data: dict) -> bool:

    # Top-level structure is valid
    if not are_talent_keys_valid(talent_data):
        return False

    # Name is valid
    if not is_name_valid(talent_data[NAME]):
        return False

    # Root is valid
    if ROOT in talent_data and not is_name_valid(talent_data[ROOT]):
        return False

    # Percent bonus is valid
    if PERCENT_BONUS in talent_data and not is_percent_bonus_valid(talent_data[PERCENT_BONUS]):
        return False

    # Absolute bonus is valid
    if ABSOLUTE_BONUS in talent_data and not is_absolute_bonus_valid(talent_data[ABSOLUTE_BONUS]):
        return False

    return True


def are_talent_keys_valid(talent_data: dict) -> bool:

    # Name is provided
    if NAME not in talent_data:
        return False

    # Data other than name and root is provided
    if set(talent_data) <= {NAME, ROOT}:
        return False

    # Keys are talent data types
    if any(key not in TALENT_DATA_TYPES for key in talent_data):
        return False

    return True


def is_name_valid(name: Any) -> bool:

    # Name is a string
    if not isinstance(name, str):
        return False

    # Name isn't too short or too long
    if not MIN_NAME_LEN <= len(name) <= MAX_NAME_LEN:
        return False

    # Name has letters
    if not any(c in string.ascii_letters for c in name):
        return False

    # Name uses only letters and spaces
    if any(c not in string.ascii_letters + " " for c in name):
        return False

    return True


def is_percent_bonus_valid(percent_bonus: Any) -> bool:
    valid = is_bonus_data_valid(percent_bonus, PercentBonus)
    return valid


def is_absolute_bonus_valid(absolute_bonus: Any) -> bool:
    valid = is_bonus_data_valid(absolute_bonus, AbsoluteBonus)
    return valid


def is_bonus_data_valid(bonus_data: Any, bonus_enum: Enum) -> bool:

    # bonus_data is a dictionary
    if not isinstance(bonus_data, dict):
        return False

    # bonus_data has items
    if not bonus_data:
        return False

    for key, lookup in bonus_data.items():

        # keys are bonus_enum members
        if key not in bonus_enum.__members__:
            return False

        # lookups are valid
        if not is_bonus_lookup_valid(lookup):
            return False

    return True


def is_bonus_lookup_valid(lookup: Any) -> bool:

    # lookup is a dictionary
    if not isinstance(lookup, dict):
        return False

    # lookup has items
    if not lookup:
        return False

    # lookup has at least one positive value
    any_pos_vals: bool = False

    for key, value in lookup.items():

        # keys are talent ranks
        if key not in TALENT_RANKS:
            return False

        # values are ints or floats
        if not isinstance(value, (int, float)):
            return False

        # values are non-negative
        if value < 0:
            return False

        any_pos_vals |= value > 0

    if not any_pos_vals:
        return False

    return True


def is_specialization_valid(spec: Any) -> bool:
    ...


def _test() -> None:
    from pathlib import Path
    fn = str(Path(__file__).parent / "Vanguard.json")
    valid = is_talent_file_valid(fn)
    print(valid)


if __name__ == "__main__":
    _test()
