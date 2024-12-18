from enum import auto, Enum


class Modifier(Enum):
    ASSAULT_RIFLE_ACCURACY  = auto()
    ASSAULT_RIFLE_DAMAGE    = auto()
    BARRIER_DURATION        = auto()
    BARRIER_REGEN           = auto()
    BARRIER_SHIELDING       = auto()
    BIOTIC_HASTE            = auto()
    BIOTIC_PROTECTION       = auto()
    DAMAGE_PROTECTION       = auto()
    FIRST_AID_HASTE         = auto()
    FIRST_AID_HEALING       = auto()
    HEALTH                  = auto()
    HEALTH_REGEN            = auto()
    HEAVY_ARMOR_DR          = auto()
    HEAVY_ARMOR_HARDENING   = auto()
    HULL_REPAIR             = auto()
    LIFT_DURATION           = auto()
    LIGHT_ARMOR_DR          = auto()
    LIGHT_ARMOR_HARDENING   = auto()
    MED_ARMOR_DR            = auto()
    MED_ARMOR_HARDENING     = auto()
    MELEE_DAMAGE            = auto()
    NEMESIS_BONUS           = auto()
    PISTOL_ACCURACY         = auto()
    PISTOL_DAMAGE           = auto()
    SHIELD_CAPACITY         = auto()
    SHOTGUN_ACCURACY        = auto()
    SHOTGUN_DAMAGE          = auto()
    SINGULARITY_RADIUS      = auto()
    SNIPER_RIFLE_ACCURACY   = auto()
    SNIPER_RIFLE_DAMAGE     = auto()
    STASIS_DURATION         = auto()
    TECH_HASTE              = auto()
    TECH_MINE_DAMAGE        = auto()
    TECH_MINE_HASTE         = auto()
    TECH_MINE_RADIUS        = auto()
    TECH_PROTECTION         = auto()
    THROW_FORCE             = auto()
    WARP_DURATION           = auto()
    WEAPON_DAMAGE           = auto()


class AbilityLevel(Enum):
    ADRENALINE_BURST    = auto()
    AI_HACKING          = auto()
    ASSASSINATION       = auto()
    BARRIER             = auto()
    CARNAGE             = auto()
    DAMPING             = auto()
    IMMUNITY            = auto()
    LIFT                = auto()
    MARKSMAN            = auto()
    NEURAL_SHOCK        = auto()
    OVERKILL            = auto()
    OVERLOAD            = auto()
    SABOTAGE            = auto()
    SHIELD_BOOST        = auto()
    SINGULARITY         = auto()
    STASIS              = auto()
    THROW               = auto()
    WARP                = auto()


class AbilitySpec(Enum):
    ADRENALINE_BURST    = auto()
    ASSASSINATION       = auto()
    BARRIER             = auto()
    IMMUNITY            = auto()
    LIFT                = auto()
    STASIS              = auto()
    WARP                = auto()
