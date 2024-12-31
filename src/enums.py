"""
Lists of names to which Talents may refer in order to set base values, bonuses,
or general features.
"""

from enum import auto, Enum


class BaseValue(Enum):
    """All ability attributes which talents may directly set the values of."""
    BARRIER_DURATION        = auto()
    BARRIER_SHIELDING       = auto()
    LIFT_DURATION           = auto()
    SINGULARITY_DURATION    = auto()
    SINGULARITY_RADIUS      = auto()
    STASIS_DURATION         = auto()
    THROW_FORCE             = auto()
    WARP_DURATION           = auto()


class Modifier(Enum):
    """All bonuses to which talents may contribute."""
    ACCURACY_REGEN          = auto()
    AI_HACKING_HASTE        = auto()
    ALL_DAMAGE              = auto()
    ALL_DURATIONS           = auto()
    ASSAULT_RIFLE_ACCURACY  = auto()
    ASSAULT_RIFLE_DAMAGE    = auto()
    BARRIER_DURATION        = auto()
    BARRIER_HASTE           = auto()
    BARRIER_REGEN           = auto()
    BARRIER_SHIELDING       = auto()
    BIOTIC_PROTECTION       = auto()
    DAMAGE_PROTECTION       = auto()
    DAMPING_HASTE           = auto()
    DAMPING_RADIUS          = auto()
    FIRST_AID_HASTE         = auto()
    FIRST_AID_HEALING       = auto()
    HEALTH                  = auto()
    HEALTH_REGEN            = auto()
    HEAVY_ARMOR_DR          = auto()
    HEAVY_ARMOR_HARDENING   = auto()
    HULL_REPAIR             = auto()
    LIFT_DURATION           = auto()
    LIFT_HASTE              = auto()
    LIGHT_ARMOR_DR          = auto()
    LIGHT_ARMOR_HARDENING   = auto()
    MAX_ACCURACY            = auto()
    MED_ARMOR_DR            = auto()
    MED_ARMOR_HARDENING     = auto()
    MELEE_DAMAGE            = auto()
    NEURAL_SHOCK_HASTE      = auto()
    OVERLOAD_HASTE          = auto()
    OVERLOAD_RADIUS         = auto()
    PISTOL_ACCURACY         = auto()
    PISTOL_COOLING          = auto()
    PISTOL_DAMAGE           = auto()
    SABOTAGE_HASTE          = auto()
    SABOTAGE_RADIUS         = auto()
    SHIELD_CAPACITY         = auto()
    SHOTGUN_ACCURACY        = auto()
    SHOTGUN_DAMAGE          = auto()
    SINGULARITY_DURATION    = auto()
    SINGULARITY_HASTE       = auto()
    SNIPER_RIFLE_ACCURACY   = auto()
    SNIPER_RIFLE_COOLING    = auto()
    SNIPER_RIFLE_DAMAGE     = auto()
    STASIS_DURATION         = auto()
    STASIS_HASTE            = auto()
    TECH_MINE_DAMAGE        = auto()
    TECH_PROTECTION         = auto()
    THROW_DAMAGE            = auto()
    THROW_FORCE             = auto()
    THROW_HASTE             = auto()
    WARP_DURATION           = auto()
    WARP_HASTE              = auto()


class AbilityLevel(Enum):
    """All abilities that may have ranks of Advanced or Master."""
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
    UNITY               = auto()
    WARP                = auto()


class Specialization(Enum):
    """All abilities which may be specialized by advanced Shepard classes."""
    ADRENALINE_BURST    = auto()
    ASSASSINATION       = auto()
    BARRIER             = auto()
    FIRST_AID           = auto()
    IMMUNITY            = auto()
    LIFT                = auto()
    NEURAL_SHOCK        = auto()
    OVERLOAD            = auto()
    SABOTAGE            = auto()
    STASIS              = auto()
    WARP                = auto()
