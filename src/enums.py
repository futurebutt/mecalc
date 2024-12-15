from enum import auto, Enum


class PercentModifier(Enum):
    HEALTH = auto()
    MELEE_DAMAGE = auto()
    PISTOL_ACCURACY = auto()
    PISTOL_DAMAGE = auto()
    WEAPON_DAMAGE = auto()


class AbilityRank(Enum):
    MARKSMAN = auto()
