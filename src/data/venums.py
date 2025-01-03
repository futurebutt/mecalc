from enum import StrEnum


class TalentDataType(StrEnum):
    NAME = "name"
    ROOT = "root"
    BASE_VALUE = "base_value"
    ABSOLUTE_BONUS = "absolute_bonus"
    PERCENT_BONUS = "percent_bonus"
    ABILITY = "ability"
    SPECIALIZATION = "specialization"


class BaseValue(StrEnum):
    ...


class AbsoluteBonus(StrEnum):
    ...


class PercentBonus(StrEnum):
    BIOTIC_PROTECTION = "BIOTIC_PROTECTION"
    PISTOL_DAMAGE = "PISTOL_DAMAGE"
    SHOTGUN_DAMAGE = "SHOTGUN_DAMAGE"


class Specialization(StrEnum):
    ADRENALINE_BURST = "ADRENALINE_BURST"
    ASSASSINATION = "ASSASSINATION"
    BARRIER = "BARRIER"
    FIRST_AID = "FIRST_AID"
    IMMUNITY = "IMMUNITY"
    LIFT = "LIFT"
    NEURAL_SHOCK = "NEURAL_SHOCK"
    OVERLOAD = "OVERLOAD"
    SABOTAGE = "SABOTAGE"
    STASIS = "STASIS"
    WARP = "WARP"
