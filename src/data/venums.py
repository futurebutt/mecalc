from enum import StrEnum


class TalentDataType(StrEnum):
    NAME = "name"
    ROOT = "root"
    BASE_VALUE = "base_value"
    ABSOLUTE_BONUS = "absolute_bonus"
    PERCENT_BONUS = "percent_bonus"
    ABILITY = "ability"
    SPECIALIZATION = "specialization"


class AbsoluteBonus(StrEnum):
    ...


class PercentBonus(StrEnum):
    BIOTIC_PROTECTION = "BIOTIC_PROTECTION"
    PISTOL_DAMAGE = "PISTOL_DAMAGE"
    SHOTGUN_DAMAGE = "SHOTGUN_DAMAGE"


class Specialization(StrEnum):
    ...


