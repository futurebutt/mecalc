import json
import string
from collections.abc import Callable
from typing import Any

from venums import AbsoluteBonus, BaseValue, PercentBonus, Specialization, TalentDataType


MIN_NAME_LENGTH = 1
MAX_NAME_LENGTH = 16
TALENT_RANKS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]


def validate_talent_file(filename: str) -> bool:
    with open(filename, "r") as f:
        talent_data: dict = json.load(f)
    return validate_talent_data(talent_data)


def validate_talent_data(talent_data: dict) -> bool:
    if TalentDataType.NAME not in talent_data:
        return False
    if set(talent_data) <= {TalentDataType.NAME, TalentDataType.ROOT}:
        return False
    if any(key not in TalentDataType for key in talent_data):
        return False

    if not validate_key(talent_data, TalentDataType.NAME, validate_name):
        return False
    if not validate_key(talent_data, TalentDataType.ROOT, validate_name):
        return False
    if not validate_key(talent_data, TalentDataType.PERCENT_BONUS, validate_percent_bonus):
        return False
    if not validate_key(talent_data, TalentDataType.ABSOLUTE_BONUS, validate_absolute_bonus):
        return False
    if not validate_key(talent_data, TalentDataType.SPECIALIZATION, validate_specialization):
        return False

    return True


def validate_key(talent_data: dict, key: str, validator_fn: Callable) -> bool:
    return key not in talent_data or validator_fn(talent_data[key])


def validate_name(name: Any) -> bool:
    if not isinstance(name, str):
        return False
    if not MIN_NAME_LENGTH <= len(name) <= MAX_NAME_LENGTH:
        return False
    if not any(c in string.ascii_letters for c in name):
        return False
    if any(c not in string.ascii_letters + " " for c in name):
        return False
    return True


def validate_base_value(base_value: Any) -> bool:
    return validate_stats(base_value, BaseValue)


def validate_percent_bonus(percent_bonus: Any) -> bool:
    return validate_stats(percent_bonus, PercentBonus)


def validate_absolute_bonus(absolute_bonus: Any) -> bool:
    return validate_stats(absolute_bonus, AbsoluteBonus)


def validate_stats(data: Any, data_enum: BaseValue | AbsoluteBonus | PercentBonus) -> bool:
    if not isinstance(data, dict) or not data:
        return False
    if any(k not in data_enum or not validate_stat_lookup(v) for k, v in data.items()):
        return False
    return True


def validate_stat_lookup(lookup: Any) -> bool:
    if not isinstance(lookup, dict) or not lookup:
        return False

    any_pos_vals: bool = False
    for key, value in lookup.items():
        if key not in TALENT_RANKS:
            return False
        if not isinstance(value, (int, float)) or value < 0:
            return False
        if value > 0:
            any_pos_vals = True

    return any_pos_vals


def validate_specialization(spec: Any) -> bool:
    if not isinstance(spec, dict) or not spec:
        return False
    if any(k not in TALENT_RANKS or v not in Specialization for k, v in spec.items()):
        return False
    return True


def _test() -> None:
    from pathlib import Path
    fn = str(Path(__file__).parent / "Vanguard.json")
    assert validate_talent_file(fn), f"{fn} is invalid!"
    print(f"Test passed!")


if __name__ == "__main__":
    _test()
