from enum import auto, Enum


class BaseValue(Enum):
    """Values of abilities before bonuses."""

    # Adrenaline Burst
    ADRENALINE_COOLDOWN = auto()
    ADRENALINE_ACC_COST = auto()
    # Immunity
    IMMUNITY_DR = auto()
    IMMUNITY_DURATION = auto()
    IMMUNITY_COOLDOWN = auto()
    # Overkill
    OVERKILL_HEAT_DOWN = auto()
    OVERKILL_DAMAGE_BONUS = auto()
    OVERKILL_DURATION = auto()
    OVERKILL_COOLDOWN = auto()
    # Marksman
    MARKSMAN_ACC_BONUS = auto()
    MARKSMAN_DAMAGE_BONUS = auto()
    MARKSMAN_HEADSHOT_BONUS = auto()
    MARKSMAN_DURATION = auto()
    MARKSMAN_COOLDOWN = auto()
    # Carnage
    CARNAGE_DPS_MULT = auto()
    CARNAGE_RADIUS = auto()
    CARNAGE_DURATION = auto()
    CARNAGE_COOLDOWN = auto()
    # Assassination
    ASSASSIN_DPS_MULT = auto()
    ASSASSIN_DURATION = auto()
    ASSASSIN_COOLDOWN = auto()
    # Shield Boost
    SHIELD_BOOST_SPS = auto()
    SHIELD_BOOST_DURATION = auto()
    SHIELD_BOOST_COOLDOWN = auto()
    SHIELD_BOOST_ACC_COST = auto()
    # Sabotage
    SABOTAGE_DAMAGE = auto()
    SABOTAGE_DPS = auto()
    SABOTAGE_DURATION = auto()
    SABOTAGE_COOLDOWN = auto()
    SABOTAGE_ACC_COST = auto()
    # Overload
    OVERLOAD_DAMAGE = auto()
    OVERLOAD_SHIELD_DAMAGE = auto()
    OVERLOAD_DR_DOWN = auto()
    OVERLOAD_DURATION = auto()
    OVERLOAD_COOLDOWN = auto()
    OVERLOAD_ACC_COST = auto()
    # AI Hacking
    AI_HACK_DURATION = auto()
    AI_HACK_COOLDOWN = auto()
    AI_HACK_ACC_COST = auto()
    # Damping
    DAMPING_DAMAGE = auto()
    DAMPING_STUN = auto()
    DAMPING_ENEMY_COOLDOWN = auto()
    DAMPING_COOLDOWN = auto()
    DAMPING_ACC_COST = auto()
    # Barrier
    BARRIER_STRENGTH = auto()
    BARRIER_DURATION = auto()
    BARRIER_COOLDOWN = auto()
    BARRIER_ACC_COST = auto()
    # Barrier Specialization
    BARRIER_REGEN = auto()
    # Lift
    LIFT_RADIUS = auto()
    LIFT_DURATION = auto()
    LIFT_COOLDOWN = auto()
    LIFT_ACC_COST = auto()
    # Singularity
    SINGULARITY_RADIUS = auto()
    SINGULARITY_DURATION = auto()
    SINGULARITY_COOLDOWN = auto()
    SINGULARITY_ACC_COST = auto()
    # Stasis
    STASIS_DURATION = auto()
    STASIS_COOLDOWN = auto()
    STASIS_ACC_COST = auto()
    # Stasis Specialization
    STASIS_ENABLE_DAMAGE = auto()
    # Throw
    THROW_FORCE = auto()
    THROW_RADIUS = auto()
    THROW_COOLDOWN = auto()
    THROW_ACC_COST = auto()
    # Warp
    WARP_DPS = auto()
    WARP_DR_DOWN = auto()
    WARP_RADIUS = auto()
    WARP_DURATION = auto()
    WARP_COOLDOWN = auto()
    WARP_ACC_COST = auto()
    # First Aid
    FIRST_AID_HEALING = auto()
    FIRST_AID_COOLDOWN = auto()
    # Neural Shock
    NEURAL_SHOCK_DAMAGE = auto()
    NEURAL_SHOCK_KNOCKOUT = auto()
    NEURAL_SHOCK_COOLDOWN = auto()
    NEURAL_SHOCK_ACC_COST = auto()
    # Unity
    UNITY_HEALTH = auto()
    UNITY_SHIELDS = auto()
    UNITY_COOLDOWN = auto()
    UNITY_ACC_COST = auto()


class BonusValue(Enum):
    """Additive percent or absolute-valued bonuses to base values."""

    # Assault Training
    MELEE_DAMAGE = auto()
    # Fitness, Soldier, Spectre Training
    HEALTH = auto()
    # Assault Rifles
    AR_DAMAGE = auto()
    AR_ACCURACY = auto()
    # Pistols
    PISTOL_DAMAGE = auto()
    PISTOL_ACCURACY = auto()
    # Shotguns
    SHOTGUN_DAMAGE = auto()
    SHOTGUN_ACCURACY = auto()
    # Sniper Rifles
    SR_DAMAGE = auto()
    SR_ACCURACY = auto()
    # Basic Armor
    LIGHT_DR = auto()
    LIGHT_HARDENING = auto()
    # Tactical Armor
    MED_DR = auto()
    MED_HARDENING = auto()
    # Combat Armor
    HEAVY_DR = auto()
    HEAVY_HARDENING = auto()
    # Decryption
    SABOTAGE_DAMAGE = auto()
    OVERLOAD_DAMAGE = auto()
    DAMPING_DAMAGE = auto()
    # Electronics
    SHIELD_CAPACITY = auto()
    HULL_REPAIR = auto()
    # Hacking
    SABOTAGE_HASTE = auto()
    OVERLOAD_HASTE = auto()
    DAMPING_HASTE = auto()
    # Damping
    SABOTAGE_RADIUS = auto()
    OVERLOAD_RADIUS = auto()
    DAMPING_RADIUS = auto()
    # First Aid
    FIRST_AID_HEALING = auto()
    # Medicine
    FIRST_AID_HASTE = auto()
    # Charm
    STORE_DISCOUNT = auto()
    # Intimidate
    SALE_BONUS = auto()
    # Spectre Training
    ALL_DAMAGE = auto()
    ALL_DURATIONS = auto()
    MAX_ACCURACY = auto()
    ACCURACY_REGEN = auto()

    # Adept
    BARRIER_HASTE = auto()
    BIOTIC_PROTECTION = auto()
    LIFT_HASTE = auto()
    THROW_HASTE = auto()
    SINGULARITY_HASTE = auto()
    STASIS_HASTE = auto()
    WARP_HASTE = auto()
    # Engineer
    HACKING_HASTE = auto()
    NEURAL_SHOCK_HASTE = auto()
    TECH_PROTECTION = auto()
    # Soldier
    HEALTH_REGEN = auto()

    # Nemesis
    BARRIER_DURATION = auto()
    THROW_DAMAGE = auto()  # This might scale implicitly with force?
    THROW_FORCE = auto()
    LIFT_DURATION = auto()
    SINGULARITY_DURATION = auto()
    STASIS_DURATION = auto()
    WARP_DURATION = auto()

    # Adrenaline Burst Specialization
    ADRENALINE_HASTE = auto()
    # Assassin Specialization
    ASSASSIN_HASTE = auto()
    MARKSMAN_HASTE = auto()
    # Immunity Specialization
    IMMUNITY_HASTE = auto()

    # Neural Shock Specialization
    NEURAL_SHOCK_DAMAGE = auto()
    NEURAL_SHOCK_DURATION = auto()
    # Overload Specialization
    OVERLOAD_DR_DOWN = auto()
    OVERLOAD_SHIELD_DAMAGE = auto()
    # Sabotage Specialization
    SABOTAGE_DPS = auto()
    SABOTAGE_DURATION = auto()

    # Barrier Specialization
    BARRIER_DURATION = auto()
    BARRIER_REGEN = auto()
    BARRIER_STRENGTH = auto()
    # Lift Specialization
    LIFT_RADIUS = auto()
    # Warp Specialization
    WARP_DPS = auto()
    WARP_RADIUS = auto()


class Feature(Enum):
    """Binary features."""
    
    # First Aid Specialization
    FIRST_AID_IGNORES_TOXIC = auto()
    FIRST_AID_REVIVES = auto()

    # Stasis Specialization
    STASIS_ENABLE_DAMAGE = auto()
