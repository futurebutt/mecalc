from enum import auto, Enum


class PercentModifier(Enum):
    ASSAULT_RIFLE_ACCURACY = auto()
    ASSAULT_RIFLE_DAMAGE = auto()
    HEALTH = auto()
    MELEE_DAMAGE = auto()
    PISTOL_ACCURACY = auto()
    PISTOL_DAMAGE = auto()
    WEAPON_DAMAGE = auto()


class AbilityLevel(Enum):
    ADRENALINE_BURST = auto()
    IMMUNITY = auto()
    MARKSMAN = auto()
    OVERKILL = auto()
