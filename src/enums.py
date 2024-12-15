from enum import auto, Enum


class PercentModifier(Enum):
    ASSAULT_RIFLE_ACCURACY  = auto()
    ASSAULT_RIFLE_DAMAGE    = auto()
    HEALTH                  = auto()
    LIGHT_ARMOR_DR          = auto()
    LIGHT_ARMOR_HARDENING   = auto()
    MELEE_DAMAGE            = auto()
    PISTOL_ACCURACY         = auto()
    PISTOL_DAMAGE           = auto()
    SHOTGUN_ACCURACY        = auto()
    SHOTGUN_DAMAGE          = auto()
    SNIPER_RIFLE_ACCURACY   = auto()
    SNIPER_RIFLE_DAMAGE     = auto()
    WEAPON_DAMAGE           = auto()


class AbilityLevel(Enum):
    ADRENALINE_BURST    = auto()
    ASSASSINATION       = auto()
    CARNAGE             = auto()
    IMMUNITY            = auto()
    MARKSMAN            = auto()
    OVERKILL            = auto()
    SHIELD_BOOST        = auto()
