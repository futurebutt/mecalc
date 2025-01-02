import json
import string
from pathlib import Path

from venums import *


TALENT_RANKS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
TALENT_DATA_TYPES = ["root", "name", "percent_bonus", "absolute_bonus", "specialization"]


def is_name_valid(name: str) -> bool:

    # Name is a string
    if not isinstance(name, str):
        return False

    # Name isn't too short or too long
    if not 1 <= len(name) <= 16:
        return False

    # Name has letters
    if not any([c in string.ascii_letters for c in name]):
        return False

    # Name uses only letters or spaces
    if any([c not in string.ascii_letters + " " for c in name]):
        return False

    return True


def is_percent_bonus_valid(pb: dict) -> bool:

    # pb is a dictionary
    if not isinstance(pb, dict):
        return False

    # pb has items
    if not pb:
        return False

    for key, lookup in pb.items():

        # key is a PercentBonus
        if key not in PercentBonus.__members__:
            return False

        # lookup is a dictionary
        if not isinstance(lookup, dict):
            return False

        # lookup's keys are talent ranks:
        if not all([k in TALENT_RANKS for k in lookup.keys()]):
            return False

        # lookup's values are ints or floats
        if not all([isinstance(v, (int, float)) for v in lookup.values()]):
            return False

        # lookup's values are non-negative
        if any([v < 0 for v in lookup.values()]):
            return False

        # at least one lookup value is positive
        if not any([v > 0 for v in lookup.values()]):
            return False

    return True


def is_talent_valid() -> bool:

    with open(Path(__file__).parent / "Vanguard.json", "r") as f:
        talent_data: dict = json.load(f)

    # Name is provided
    if "name" not in talent_data:
        return False

    # Enough data is provided
    if len(talent_data) <= 1:
        return False

    # Data types are valid
    if any([data not in TALENT_DATA_TYPES for data in talent_data]):
        return False

    # Name is valid
    if not is_name_valid(talent_data["name"]):
        return False

    # Percent-bonus data is valid
    if not is_percent_bonus_valid(talent_data["percent_bonus"]):
        return False

    return True


if __name__ == "__main__":
    valid = is_talent_valid()
    print(valid)
