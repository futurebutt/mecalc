import json
from enum import StrEnum
from pathlib import Path

from venums import *


def get_highest_value(data: dict, data_type: TalentDataType, value_type: StrEnum, rank: int):
    ...


def get_base_value(data, value_type, rank):
    out = None
    lookup = data[TalentDataType.BASE_VALUE][value_type]
    for threshold, value in lookup.items():
        if rank >= threshold:
            out = value
    return out


def get_percent_bonus(data, value_type, rank):
    out = None
    lookup = data[TalentDataType.PERCENT_BONUS][value_type]
    for threshold, value in lookup.items():
        if rank >= threshold:
            out = value
    return out


def get_ability_level(data, ability, rank):
    out = 0
    lookup = data[TalentDataType.ABILITY][ability]
    for threshold, level in lookup.items():
        if rank >= threshold:
            out = level
    return out


def get_specialized(data, spec, rank):
    threshold = data[TalentDataType.SPECIALIZATION][spec]
    return rank >= threshold


def summarize_Barrier(rank: int) -> str:
    with open(Path(__file__).parent / "Barrier.json") as file:
        data: dict = json.load(file)
    
    level = get_ability_level(data, Ability.BARRIER, rank)
    duration = get_base_value(data, BaseValue.BARRIER_DURATION, rank)
    shielding = get_base_value(data, BaseValue.BARRIER_SHIELDING, rank)
    recharge = {1: 60, 2: 50, 3: 40}[level]
    accuracy_cost = 0.80
    regeneration = 0

    duration_pct_bonus = get_percent_bonus(data, PercentBonus.BARRIER_DURATION, rank)
    haste = get_percent_bonus(data, PercentBonus.BARRIER_HASTE, rank)
    shielding_pct_bonus = 0

    if specialized := get_specialized(data, Specialization.BARRIER, rank):
        duration_pct_bonus += 0.25
        shielding_pct_bonus += 0.25
        regeneration = 40
    
    duration *= (1 + duration_pct_bonus)
    shielding *= (1 + shielding_pct_bonus)
    cooldown *= (1 - haste)
    
    ...
