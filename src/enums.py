from enum import auto, Enum


class Modifier(Enum):
    ASSAULT_RIFLE_ACCURACY  = auto()
    ASSAULT_RIFLE_DAMAGE    = auto()
    FIRST_AID_HEALING       = auto()
    HEALTH                  = auto()
    HEALTH_REGEN            = auto()
    HEAVY_ARMOR_DR          = auto()
    HEAVY_ARMOR_HARDENING   = auto()
    HULL_REPAIR             = auto()
    LIGHT_ARMOR_DR          = auto()
    LIGHT_ARMOR_HARDENING   = auto()
    MED_ARMOR_DR            = auto()
    MED_ARMOR_HARDENING     = auto()
    MELEE_DAMAGE            = auto()
    PISTOL_ACCURACY         = auto()
    PISTOL_DAMAGE           = auto()
    SHIELD_CAPACITY         = auto()
    SHOTGUN_ACCURACY        = auto()
    SHOTGUN_DAMAGE          = auto()
    SNIPER_RIFLE_ACCURACY   = auto()
    SNIPER_RIFLE_DAMAGE     = auto()
    TECH_MINE_DAMAGE        = auto()
    TECH_MINE_HASTE         = auto()
    TECH_MINE_RADIUS        = auto()
    WEAPON_DAMAGE           = auto()


class AbilityLevel(Enum):
    ADRENALINE_BURST    = auto()
    AI_HACKING          = auto()
    ASSASSINATION       = auto()
    CARNAGE             = auto()
    DAMPING             = auto()
    IMMUNITY            = auto()
    MARKSMAN            = auto()
    OVERKILL            = auto()
    OVERLOAD            = auto()
    SABOTAGE            = auto()
    SHIELD_BOOST        = auto()


class AbilitySpec(Enum):
    ASSASSINATION   = auto()
    IMMUNITY        = auto()
