from collections.abc import Iterable

from enums import AbilityLevel, BaseValue, Specialization, Modifier
from talents import Talent


def calculate_bonus(talents: Iterable[Talent], dependencies: Iterable[Modifier]) -> float:
    value: float = 0.0
    for talent in talents:
        modifiers = talent.get_modifiers()
        for dep in dependencies:
            value += modifiers.get(dep, 0)
    return value


def get_ability_level(talents: Iterable[Talent], dependency: AbilityLevel) -> int:
    rank: int = 0
    for talent in talents:
        abilities = talent.get_abilities()
        rank = max(rank, abilities.get(dependency, 0))
    return rank


def get_ability_specialization(talents: Iterable[Talent], dependency: Specialization) -> bool:
    for talent in talents:
        abilities = talent.get_abilities()
        if abilities.get(dependency, False):
            return True
    else:
        return False


def get_highest_value(talents, value_type, least_possible=0):

    highest_value = least_possible

    for talent in talents:
        modifiers = talent.get_modifiers()
        highest_value = max(highest_value, modifiers.get(value_type, 0))

    return highest_value


def truncate(value: float) -> int | float:
    if value % 1 == 0:
        value = int(value)
    else:
        value = round(value, 3)
    return value


def format_title(name: str, level: int) -> str:
    fstr = name + {1: "", 2: " (Advanced)", 3: " (Master)"}[level]
    return fstr


def format_accuracy_cost(value: float) -> str:
    fstr = f"Accuracy Cost {truncate(value * 100)}%"
    return fstr


def format_accuracy_bonus(value: float) -> str:
    if value == 0:
        return ""
    fstr = f"Accuracy + {truncate(value * 100)}%"
    return fstr


def format_damage_bonus(value: float) -> str:
    if value == 0:
        return ""
    fstr = f"Damage + {truncate(value * 100)}%"
    return fstr


def format_damage_reduction(value: float) -> str:
    if value == 0:
        return ""
    fstr = f"Damage Protection + {truncate(value * 100)}%"
    return fstr


def format_duration(value: int | float) -> str:
    fstr = f"Duration {truncate(value)} sec"
    return fstr


def format_hardening(value: float) -> str:
    if value == 0:
        return ""
    fstr = f"Hardening + {truncate(value * 100)}%"
    return fstr


def format_health_bonus(value: float) -> str:
    if value == 0:
        return ""
    fstr = f"Health + {truncate(value * 100)}%"
    return fstr


def format_percent_dps(value: float):
    fstr = f"Damage {truncate(value * 100)}% DPS"
    return fstr


def format_radius(value: int | float) -> str:
    fstr = f"Radius {truncate(value)}m"
    return fstr


def format_recharge(seconds: int | float) -> str:
    fstr = f"Recharge {truncate(seconds)} sec"
    return fstr


def summarize(title: str, *desc: str, indent: int = 4) -> str:
    return "\n".join([title] + [f"{' ' * indent}{d}" for d in desc if d])


def summarize_Adrenaline_Burst(talents: Iterable[Talent]) -> str:

    level = get_ability_level(talents, AbilityLevel.ADRENALINE_BURST)
    if level == 0:
        return ""

    # Base values
    recharge = {1: 120, 2: 90, 3: 45}[level]
    accuracy_cost = 0.30
    # Bonuses
    haste = 0
    # Apply spec
    if specialized := get_ability_specialization(talents, Specialization.ADRENALINE_BURST):
        haste += 0.25
    # Apply bonuses
    recharge *= (1 - haste)

    summary = summarize(
        format_title("Adrenaline Burst", level),
        "Adrenaline Burst Specialization" if specialized else "",
        format_recharge(recharge),
        format_accuracy_cost(accuracy_cost),
    )
    return summary


def summarize_AI_Hacking(talents: Iterable[Talent]) -> str:

    level = get_ability_level(talents, AbilityLevel.AI_HACKING)
    if level == 0:
        return ""

    # Base values
    duration = {1: 20, 2: 25, 3: 30}[level]
    recharge = {1: 60, 2: 50, 3: 40}[level]
    accuracy_cost = 0.80
    # Bonuses
    duration_bonus = calculate_bonus(talents, (Modifier.ALL_DURATIONS, ))
    haste = calculate_bonus(talents, (Modifier.AI_HACKING_HASTE, ))
    # Apply bonuses
    duration *= (1 + duration_bonus)
    recharge *= (1 - haste)

    summary = summarize(
        format_title("AI Hacking", level),
        format_duration(duration),
        format_recharge(recharge),
        format_accuracy_cost(accuracy_cost),
    )
    return summary


def summarize_Assassination(talents: Iterable[Talent]) -> str:

    level = get_ability_level(talents, AbilityLevel.ASSASSINATION)
    if level == 0:
        return ""

    # Base values
    percent_dps = {1: 2.00, 2: 2.50, 3: 3.00}[level]
    duration = 6
    recharge = 45
    # Bonuses
    haste = 0
    # Apply spec
    if specialized := get_ability_specialization(talents, Specialization.ASSASSINATION):
        haste += 0.25
    # Apply bonuses
    recharge *= (1 - haste)

    summary = summarize(
        format_title("Assassination", level),
        "Assassination Specialization" if specialized else "",
        format_percent_dps(percent_dps),
        format_duration(duration),
        format_recharge(recharge),
    )
    return summary


def summarize_Assault_Rifle(talents: Iterable[Talent]) -> str:

    # Bonuses
    accuracy_bonus = calculate_bonus(talents, (Modifier.ASSAULT_RIFLE_ACCURACY, ))
    damage_bonus = calculate_bonus(talents, (Modifier.ASSAULT_RIFLE_DAMAGE, Modifier.ALL_DAMAGE))
    # Don't bother if no bonuses
    if damage_bonus == accuracy_bonus == 0:
        return ""

    summary = summarize(
        "Assault Rifles",
        format_damage_bonus(damage_bonus),
        format_accuracy_bonus(accuracy_bonus)
    )
    return summary


def summarize_Barrier(talents: Iterable[Talent]) -> str:

    level = get_ability_level(talents, AbilityLevel.BARRIER)
    if level == 0:
        return ""
    
    # Base values
    duration = get_highest_value(talents, BaseValue.BARRIER_DURATION)
    shielding = get_highest_value(talents, BaseValue.BARRIER_SHIELDING)
    recharge = {1: 60, 2: 50, 3: 40}[level]
    acc_cost = 0.80
    regen = 0
    # Bonuses
    duration_bonus = calculate_bonus(talents, (Modifier.BARRIER_DURATION, Modifier.ALL_DURATIONS))
    haste = calculate_bonus(talents, (Modifier.BARRIER_HASTE, ))
    shielding_bonus = 0
    # Apply spec
    if specialized := get_ability_specialization(talents, Specialization.BARRIER):
        duration_bonus += 0.25
        shielding_bonus += 0.25
        regen = 40
    # Apply bonuses
    duration *= (1.00 + duration_bonus)
    shielding *= (1.00 + shielding_bonus)
    recharge *= (1.00 - haste)

    summary = summarize(
        format_title("Barrier", level),
        "Barrier Specialization" if specialized else "",
        f"Shielding {shielding}",
        format_duration(duration),
        f"Regen {regen} pts / sec" if regen else "",
        format_recharge(recharge),
        format_accuracy_cost(acc_cost),
    )
    return summary


def summarize_Carnage(talents: Iterable[Talent]) -> str:

    level = get_ability_level(talents, AbilityLevel.CARNAGE)
    if level == 0:
        return ""

    # Base values
    percent_dps = {1: 2.00, 2: 2.25, 3: 2.50}[level]
    radius = {1: 2, 2: 2.5, 3: 3}[level]
    duration = 6
    recharge = 45
    # Bonuses
    duration_bonus = calculate_bonus(talents, (Modifier.ALL_DURATIONS, ))
    # Apply bonuses
    duration *= (1 + duration_bonus)

    summary = summarize(
        format_title("Carnage", level),
        format_percent_dps(percent_dps),
        format_radius(radius),
        format_duration(duration),
        format_recharge(recharge),
    )
    return summary


def summarize_Damping(talents: Iterable[Talent]) -> str:

    level = get_ability_level(talents, AbilityLevel.DAMPING)
    if level == 0:
        return ""

    # Base values
    radius = {1: 6, 2: 8, 3: 10}[level]
    recharge = {1: 60, 2: 50, 3: 40}[level]
    tech_mine_damage = {1: 50, 2: 100, 3: 100}[level]
    accuracy_cost = 0.60
    stun_duration = 3
    # Bonuses
    haste = calculate_bonus(talents, (Modifier.DAMPING_HASTE, ))
    radius_bonus = calculate_bonus(talents, (Modifier.DAMPING_RADIUS, ))
    stun_bonus = calculate_bonus(talents, (Modifier.ALL_DURATIONS, ))
    tmd_bonus = calculate_bonus(talents, (Modifier.TECH_MINE_DAMAGE, Modifier.ALL_DAMAGE))
    # Apply bonuses
    radius *= (1 + radius_bonus)
    recharge *= (1 - haste)
    stun_duration *= (1 + stun_bonus)
    tech_mine_damage *= (1 + tmd_bonus)

    summary = summarize(
        format_title("Damping", level),
        f"Tech Mine Damage {truncate(tech_mine_damage)}",
        f"Stun {stun_duration} sec",
        format_radius(radius),
        format_recharge(recharge),
        format_accuracy_cost(accuracy_cost),
    )
    return summary


def summarize_First_Aid(talents: Iterable[Talent]) -> str:

    # Base values
    healing = 40
    recharge = 20
    # Bonuses
    healing_bonus = calculate_bonus(talents, (Modifier.FIRST_AID_HEALING, ))  # absolute value, not percent
    haste = calculate_bonus(talents, (Modifier.FIRST_AID_HASTE, ))
    # Apply spec
    if specialized := get_ability_specialization(talents, Specialization.FIRST_AID):
        healing_bonus += 80
    # Apply bonuses
    healing += healing_bonus
    recharge *= (1 - haste)

    summary = summarize(
        "First Aid",
        "First Aid Specialization:" if specialized else "",
        "    Ignore toxic damage" if specialized else "",
        "    Revive fallen party members" if specialized else "",
        f"Health Restored {truncate(healing)}",
        format_recharge(recharge),
    )
    return summary


def summarize_Heavy_Armor(talents: Iterable[Talent]) -> str:

    # Bonuses
    damage_reduction = calculate_bonus(talents, (Modifier.HEAVY_ARMOR_DR, ))
    hardening = calculate_bonus(talents, (Modifier.HEAVY_ARMOR_HARDENING, ))
    # Don't bother if no bonuses
    if damage_reduction == hardening == 0:
        return ""

    summary = summarize(
        "Heavy Armor",
        format_damage_reduction(damage_reduction),
        format_hardening(hardening),
    )
    return summary


def summarize_Immunity(talents: Iterable[Talent]) -> str:

    level = get_ability_level(talents, AbilityLevel.IMMUNITY)
    if level == 0:
        return ""

    # Base values
    damage_reduction_mult = {1: 0.75, 2: 0.85, 3: 0.90}[level]
    duration = 6
    recharge = 45
    # Bonuses
    duration_bonus = calculate_bonus(talents, (Modifier.ALL_DURATIONS, ))
    haste = 0
    # Apply spec
    if specialized := get_ability_specialization(talents, Specialization.IMMUNITY):
        haste += 0.25
    # apply bonuses
    duration *= (1 + duration_bonus)
    recharge *= (1 - haste)

    summary = summarize(
        format_title("Immunity", level),
        "Immunity Specialization" if specialized else "",
        f"Damage Reduction {truncate(damage_reduction_mult * 100)}%",
        format_duration(duration),
        format_recharge(recharge),
    )

    return summary


def summarize_Lift(talents: Iterable[Talent]) -> str:

    level = get_ability_level(talents, AbilityLevel.LIFT)
    if level == 0:
        return ""

    # Base values
    duration = get_highest_value(talents, BaseValue.LIFT_DURATION)
    accuracy_cost = {1: 0.80, 2: 0.60, 3: 0.40}[level]
    radius = {1: 4, 2: 5, 3: 6}[level]
    recharge = {1: 60, 2: 50, 3: 40}[level]
    # Bonuses
    duration_bonus = calculate_bonus(talents, (Modifier.LIFT_DURATION, Modifier.ALL_DURATIONS))
    haste = calculate_bonus(talents, (Modifier.LIFT_HASTE, ))
    radius_bonus = 0  # absolute
    # Apply spec
    if specialized := get_ability_specialization(talents, Specialization.LIFT):
        radius_bonus += 4
    # Apply bonuses
    duration *= (1 + duration_bonus)
    radius += radius_bonus
    recharge *= (1 - haste)

    summary = summarize(
        format_title("Lift", level),
        "Lift Specialization" if specialized else "",
        format_duration(duration),
        format_radius(radius),
        format_recharge(recharge),
        format_accuracy_cost(accuracy_cost),
    )
    return summary


def summarize_Light_Armor(talents: Iterable[Talent]) -> str:

    # Bonuses
    damage_reduction = calculate_bonus(talents, (Modifier.LIGHT_ARMOR_DR, ))
    hardening = calculate_bonus(talents, (Modifier.LIGHT_ARMOR_HARDENING, ))
    # Don't bother if no bonuses
    if damage_reduction == hardening == 0:
        return ""

    summary = summarize(
        "Light Armor",
        format_damage_reduction(damage_reduction),
        format_hardening(hardening),
    )
    return summary


def summarize_Mako(talents: Iterable[Talent]) -> str:

    # Bonuses
    # TODO: Find out what the base repair value is and display it.
    repair = calculate_bonus(talents, (Modifier.HULL_REPAIR, ))
    # Don't bother if no bonuses
    if repair == 0:
        return ""

    summary = summarize(
        "Mako",
        f"Mako Hull Repair + {repair}",
    )
    return summary


def summarize_Marksman(talents: Iterable[Talent]) -> str:

    level = get_ability_level(talents, AbilityLevel.MARKSMAN)
    if level == 0:
        return ""

    # Base values
    damage = {1: 0.25, 2: 0.50, 3: 0.75}[level]
    headshot_damage = {1: 0.50, 2: 0.75, 3: 1.00}[level]
    accuracy = 0.60
    duration = 6
    recharge = 45
    # Bonuses
    haste = 0
    # Apply spec
    if specialized := get_ability_specialization(talents, Specialization.ASSASSINATION):
        haste += 0.25
    # Apply bonuses
    recharge *= (1 - haste)

    summary = summarize(
        format_title("Marksman", level),
        "Assassination Specialization" if specialized else "",
        format_accuracy_bonus(accuracy),
        format_damage_bonus(damage),
        f"Headshot Damage + {truncate(headshot_damage * 100)}%",
        format_duration(duration),
        format_recharge(recharge),
    )
    return summary


def summarize_Medium_Armor(talents: Iterable[Talent]) -> str:

    # Bonuses
    damage_reduction = calculate_bonus(talents, (Modifier.MED_ARMOR_DR, ))
    hardening = calculate_bonus(talents, (Modifier.MED_ARMOR_HARDENING, ))
    # Don't bother if no bonuses
    if damage_reduction == hardening == 0:
        return ""

    summary = summarize(
        "Medium Armor",
        format_damage_reduction(damage_reduction),
        format_hardening(hardening),
    )
    return summary


def summarize_Neural_Shock(talents: Iterable[Talent]) -> str:

    level = get_ability_level(talents, AbilityLevel.NEURAL_SHOCK)
    if level == 0:
        return ""

    # Base values
    knockout = {1: 1, 2: 3, 3: 5}[level]
    toxic_damage = {1: 40, 2: 80, 3: 120}[level]
    acc_cost = 0.60
    recharge = 45
    # Bonuses
    haste = calculate_bonus(talents, (Modifier.NEURAL_SHOCK_HASTE, ))
    knockout_bonus = calculate_bonus(talents, (Modifier.ALL_DURATIONS, ))
    td_pct_bonus = calculate_bonus(talents, (Modifier.ALL_DAMAGE, ))
    td_abs_bonus = 0
    # Apply spec
    if specialized := get_ability_specialization(talents, Specialization.NEURAL_SHOCK):
        knockout_bonus += 0.25
        td_abs_bonus += 40
    # Apply bonuses
    knockout *= (1 + knockout_bonus)
    recharge *= (1 - haste)
    toxic_damage = (toxic_damage + td_abs_bonus) * (1 + td_pct_bonus)

    summary = summarize(
        format_title("Neural Shock", level),
        "Neural Shock Specialization" if specialized else "",
        f"Toxic Damage {toxic_damage}",
        f"Knockout {knockout} sec",
        format_recharge(recharge),
        format_accuracy_cost(acc_cost),
    )
    return summary


def summarize_Overkill(talents: Iterable[Talent]) -> str:

    level = get_ability_level(talents, AbilityLevel.OVERKILL)
    if level == 0:
        return ""

    # Base values
    cooling = {1: 0.80, 2: 0.90, 3: 1.00}[level]
    damage = {1: 0.50, 2: 0.75, 3: 1.00}[level]
    duration = 6
    recharge = 45
    # Bonuses
    duration_bonus = calculate_bonus(talents, (Modifier.ALL_DURATIONS, ))
    # Apply bonuses
    duration *= (1 + duration_bonus)
    
    summary = summarize(
        format_title("Overkill", level),
        f"Cooling {truncate(cooling * 100)}%",
        format_damage_bonus(damage),
        format_duration(duration),
        format_recharge(recharge),
    )
    return summary


def summarize_Overload(talents: Iterable[Talent]) -> str:

    level = get_ability_level(talents, AbilityLevel.OVERLOAD)
    if level == 0:
        return ""

    # Base values
    radius = {1: 6, 2: 8, 3: 10}[level]
    recharge = {1: 60, 2: 50, 3: 40}[level]
    shield_damage = {1: 200, 2: 400, 3: 600}[level]
    sunder = {1: 0.20, 2: 0.25, 3: 0.30}[level]
    tech_mine_damage = {1: 50, 2: 100, 3: 150}[level]
    accuracy_cost = 0.60
    duration = 10
    # Bonuses
    duration_bonus = calculate_bonus(talents, (Modifier.ALL_DURATIONS, ))
    haste = calculate_bonus(talents, (Modifier.OVERLOAD_HASTE, ))
    radius_abs_bonus = 0
    radius_pct_bonus = calculate_bonus(talents, (Modifier.OVERLOAD_RADIUS, ))
    shd_abs_bonus = 0
    shd_pct_bonus = calculate_bonus(talents, (Modifier.ALL_DAMAGE, ))
    sunder_flat_bonus = 0
    tmd_abs_bonus = 0
    tmd_pct_bonus = calculate_bonus(talents, (Modifier.TECH_MINE_DAMAGE, Modifier.ALL_DAMAGE))
    # Apply spec
    if specialized := get_ability_specialization(talents, Specialization.OVERLOAD):
        radius_abs_bonus += 2
        shd_abs_bonus += 200
        sunder_flat_bonus += 0.05
        tmd_abs_bonus += 50
    # Apply bonuses
    duration *= (1.00 + duration_bonus)
    radius = (radius + radius_abs_bonus) * (1.00 + radius_pct_bonus)
    recharge *= (1.00 - haste)
    shield_damage = (shield_damage + shd_abs_bonus) * (1.00 + shd_pct_bonus)
    sunder += sunder_flat_bonus
    tech_mine_damage = (tech_mine_damage + tmd_abs_bonus) * (1.00 + tmd_pct_bonus)

    summary = summarize(
        format_title("Overload", level),
        "Overload Specialization" if specialized else "",
        f"Tech Mine Damage {truncate(tech_mine_damage)}",
        f"Shield Damage {shield_damage}",
        f"Reduce Damage Protection {truncate(sunder * 100)}%",
        format_radius(radius),
        format_duration(duration),
        format_recharge(recharge),
        format_accuracy_cost(accuracy_cost),
    )
    return summary


def summarize_Pistol(talents: Iterable[Talent]) -> str:

    # Bonuses
    accuracy_bonus = calculate_bonus(talents, (Modifier.PISTOL_ACCURACY, ))
    cooling = calculate_bonus(talents, (Modifier.PISTOL_COOLING, ))
    damage = calculate_bonus(talents, (Modifier.PISTOL_DAMAGE, Modifier.ALL_DAMAGE))
    # Don't bother if no bonuses
    if damage == accuracy_bonus == cooling == 0:
        return ""

    summary = summarize(
        "Pistol",
        format_damage_bonus(truncate(damage)),
        format_accuracy_bonus(truncate(accuracy_bonus)),
        f"Cooling + {truncate(cooling * 100)}%" if cooling else "",
    )
    return summary


def summarize_Sabotage(talents: Iterable[Talent]) -> str:

    level = get_ability_level(talents, AbilityLevel.SABOTAGE)
    if level == 0:
        return ""

    # Base values
    burn_dps = {1: 2, 2: 3, 3: 4}[level]
    duration = {1: 15, 2: 20, 3: 25}[level]
    radius = {1: 6, 2: 8, 3: 10}[level]
    recharge = {1: 60, 2: 50, 3: 40}[level]
    tech_mine_damage = {1: 50, 2: 100, 3: 150}[level]
    accuracy_cost = 0.60
    # Bonuses
    dps_abs_bonus = 0
    dps_pct_bonus = calculate_bonus(talents, (Modifier.ALL_DAMAGE))
    duration_abs_bonus = 0
    duration_pct_bonus = calculate_bonus(talents, (Modifier.ALL_DURATIONS, ))
    radius_abs_bonus = 0
    radius_pct_bonus = calculate_bonus(talents, (Modifier.SABOTAGE_RADIUS, ))
    haste = calculate_bonus(talents, (Modifier.SABOTAGE_HASTE, ))
    tmd_abs_bonus = 0
    tmd_pct_bonus = calculate_bonus(talents, (Modifier.TECH_MINE_DAMAGE, Modifier.ALL_DAMAGE))
    # Apply spec
    if specialized := get_ability_specialization(talents, Specialization.SABOTAGE):
        dps_abs_bonus += 1
        duration_abs_bonus += 5
        radius_abs_bonus += 2
        tmd_abs_bonus += 50
    # Apply bonuses
    burn_dps = (burn_dps + dps_abs_bonus) * (1 + dps_pct_bonus)
    tech_mine_damage = (tech_mine_damage + tmd_abs_bonus) * (1 + tmd_pct_bonus)
    radius = (radius + radius_abs_bonus) * (1 + radius_pct_bonus)
    duration = (duration + duration_abs_bonus) * (1 + duration_pct_bonus)
    recharge *= (1 - haste)

    summary = summarize(
        format_title("Sabotage", level),
        "Sabotage Specialization" if specialized else "",
        f"Tech Mine Damage {truncate(tech_mine_damage)}",
        f"Burn DPS {burn_dps}",
        format_radius(radius),
        format_duration(duration),
        format_recharge(recharge),
        format_accuracy_cost(accuracy_cost),
    )
    return summary


def summarize_Shepard(talents: Iterable[Talent]) -> str:

    # Bonuses
    acc_regen = calculate_bonus(talents, (Modifier.ACCURACY_REGEN, ))
    bio_prot = calculate_bonus(talents, (Modifier.BIOTIC_PROTECTION, ))
    health_regen = calculate_bonus(talents, (Modifier.HEALTH_REGEN, ))
    hp = calculate_bonus(talents, (Modifier.HEALTH, ))
    max_acc = calculate_bonus(talents, (Modifier.MAX_ACCURACY, ))
    melee = calculate_bonus(talents, (Modifier.MELEE_DAMAGE, Modifier.ALL_DAMAGE))
    shields = calculate_bonus(talents, (Modifier.SHIELD_CAPACITY, ))
    tech_prot = calculate_bonus(talents, (Modifier.TECH_PROTECTION, ))
    # Don't bother if no bonuses
    if acc_regen == bio_prot == health_regen == hp == max_acc == melee == shields == tech_prot == 0:
        return ""

    summary = summarize(
        "Shepard",
        format_health_bonus(hp),
        f"Shields + {truncate(shields)}" if shields else "",
        f"Tech Protection + {truncate(tech_prot * 100)}%" if tech_prot else "",
        f"Biotic Protection + {truncate(bio_prot * 100)}%" if bio_prot else "",
        f"Health Regen {truncate(health_regen)} per sec" if health_regen else "",
        f"Melee Damage + {truncate(melee * 100)}%" if melee else "",
        f"Max Accuracy + {truncate(max_acc)}%" if max_acc else "",
        f"Accuracy Regen + {truncate(acc_regen)}%" if acc_regen else "",
    )
    return summary


def summarize_Shield_Boost(talents: Iterable[Talent]) -> str:

    level = get_ability_level(talents, AbilityLevel.SHIELD_BOOST)
    if level == 0:
        return ""

    shields_restored = {1: 0.30, 2: 0.40, 3: 0.50}[level]
    accuracy_cost = 0.30
    duration = 2
    recharge = 45

    summary = summarize(
        format_title("Shield Boost", level),
        f"Shields Restored {truncate(shields_restored * 100)}%",
        format_duration(duration),
        format_recharge(recharge),
        format_accuracy_cost(accuracy_cost),
    )
    return summary


def summarize_Shotgun(talents: Iterable[Talent]) -> str:

    title = "Shotgun"
    damage = calculate_bonus(talents, (Modifier.SHOTGUN_DAMAGE, Modifier.ALL_DAMAGE))
    accuracy = calculate_bonus(talents, (Modifier.SHOTGUN_ACCURACY, ))
    if damage == accuracy == 0:
        return ""

    summary = summarize(
        title,
        format_damage_bonus(truncate(damage)),
        format_accuracy_bonus(truncate(accuracy))
    )
    return summary


def summarize_Singularity(talents: Iterable[Talent]) -> str:

    level = get_ability_level(talents, AbilityLevel.SINGULARITY)
    if level == 0:
        return ""

    title = "Singularity"

    radius = calculate_bonus(talents, (Modifier.SINGULARITY_RADIUS, ))
    haste = calculate_bonus(talents, (Modifier.SINGULARITY_HASTE, ))
    duration_bonus = calculate_bonus(talents, (Modifier.SINGULARITY_DURATION, ))

    duration = {1: 4, 2: 6, 3: 8}[level]
    duration *= (1.00 + duration_bonus)
    recharge = {1: 60, 2: 50, 3: 40}[level]
    recharge *= (1.00 - haste)

    acc_cost = 0.80

    summary = summarize(
        format_title(title, level),
        format_radius(radius),
        format_duration(duration),
        format_recharge(recharge),
        format_accuracy_cost(acc_cost),
    )
    return summary


def summarize_Sniper_Rifles(talents: Iterable[Talent]) -> str:

    title = "Sniper Rifles"
    damage = calculate_bonus(talents, (Modifier.SNIPER_RIFLE_DAMAGE, Modifier.ALL_DAMAGE))
    accuracy = calculate_bonus(talents, (Modifier.SNIPER_RIFLE_ACCURACY, ))
    cooling = calculate_bonus(talents, (Modifier.SNIPER_RIFLE_COOLING, ))
    if damage == accuracy == cooling == 0:
        return ""

    summary = summarize(
        title,
        format_damage_bonus(damage),
        format_accuracy_bonus(accuracy),
        f"Cooling + {truncate(cooling * 100)}%" if cooling else "",
    )
    return summary


def summarize_Stasis(talents: Iterable[Talent]) -> str:

    level = get_ability_level(talents, AbilityLevel.STASIS)
    if level == 0:
        return ""

    title = "Stasis"

    duration = get_highest_value(talents, BaseValue.STASIS_DURATION)
    duration_bonus = calculate_bonus(talents, (Modifier.STASIS_DURATION, Modifier.ALL_DURATIONS))
    duration *= (1.00 + duration_bonus)
    haste = calculate_bonus(talents, (Modifier.STASIS_HASTE, ))

    recharge = {1: 60, 2: 50, 3: 40}[level]
    recharge *= (1.00 - haste)

    acc_cost = 0.80

    specialized = get_ability_specialization(talents, Specialization.STASIS)

    summary = summarize(
        format_title(title, level),
        "Stasis Specialization:" if specialized else "",
        "    Damage enemies in Stasis" if specialized else "",
        format_duration(duration),
        format_recharge(recharge),
        format_accuracy_cost(acc_cost),
    )
    return summary


def summarize_Throw(talents: Iterable[Talent]) -> str:

    level = get_ability_level(talents, AbilityLevel.THROW)
    if level == 0:
        return ""

    title = "Throw"

    force = get_highest_value(talents, BaseValue.THROW_FORCE)
    force_bonus = calculate_bonus(talents, ( Modifier.THROW_FORCE, ))
    force *= (1.00 + force_bonus)
    damage = calculate_bonus(talents, (Modifier.THROW_DAMAGE, Modifier.ALL_DAMAGE))
    haste = calculate_bonus(talents, (Modifier.THROW_HASTE, ))

    radius = {1: 4, 2: 5, 3: 6}[level]
    recharge = {1: 60, 2: 50, 3: 40}[level]
    recharge *= (1.00 - haste)
    acc_cost = {1: 0.60, 2: 0.45, 3: 0.30}[level]

    summary = summarize(
        format_title(title, level),
        f"Force {truncate(force)}N",
        format_damage_bonus(damage),
        format_radius(radius),
        format_recharge(recharge),
        format_accuracy_cost(acc_cost),
    )
    return summary


def summarize_Unity(talents: Iterable[Talent]) -> str:

    level = get_ability_level(talents, AbilityLevel.UNITY)
    if level == 0:
        return ""

    title = "Unity"
    health = {1: 0.15, 2: 0.20, 3: 0.30}[level]
    shields = {1: 0.40, 2: 0.60, 3: 1.00}[level]
    recharge = {1: 150, 2: 120, 3: 90}[level]
    acc_cost = 0.45

    summary = summarize(
        format_title(title, level),
        f"Health {truncate(health * 100)}%",
        f"Shields {truncate(shields * 100)}%",
        format_recharge(recharge),
        format_accuracy_cost(acc_cost),
    )
    return summary


def summarize_Warp(talents: Iterable[Talent]) -> str:

    level = get_ability_level(talents, AbilityLevel.WARP)
    if level == 0:
        return ""

    title = "Warp"

    dps = {1: 6, 2: 8, 3: 10}[level]
    sunder = {1: 0.50, 2: 0.60, 3: 0.75}[level]
    radius = {1: 4, 2: 5, 3: 6}[level]
    recharge = {1: 60, 2: 50, 3: 40}[level]

    acc_cost = 0.80

    duration = get_highest_value(talents, BaseValue.WARP_DURATION)
    duration_bonus = calculate_bonus(talents, (Modifier.WARP_DURATION, Modifier.ALL_DURATIONS))
    haste = calculate_bonus(talents, (Modifier.WARP_HASTE, ))
    dps_bonus = calculate_bonus(talents, (Modifier.ALL_DAMAGE, ))

    if specialized := get_ability_specialization(talents, Specialization.WARP):
        radius += 2
        dps_bonus += 0.25

    dps *= (1 + dps_bonus)
    duration *= (1 + duration_bonus)
    recharge *= (1.00 - haste)

    summary = summarize(
        format_title(title, level),
        "Warp Specialization" if specialized else "",
        f"DPS {dps}",
        f"Reduce Damage Protection {truncate(sunder * 100)}%",
        format_radius(radius),
        format_duration(duration),
        format_recharge(recharge),
        format_accuracy_cost(acc_cost),
    )
    return summary
