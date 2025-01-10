from collections.abc import Iterable

from enums import Ability, AbsoluteBonus, BaseValue, Specialization, PercentBonus
from talents import Talent


def format_ability_title(name: str, rank: int, spec: bool = False) -> str:
    elements: list[str] = [name]
    if rank == 2:
        elements.append("(Advanced)")
    elif rank == 3:
        elements.append("(Master)")
    if spec:
        elements.append("(Specialized)")
    return " ".join(elements)


def format_number(value: float) -> str:
    if value % 1 == 0:
        return str(int(value))
    else:
        return str(round(value, 3))


def format_percent(name: str, dec: float) -> str:
    return f"{name} {format_number(100 * dec)}%"


def format_plus_percent(name: str, dec: float) -> str:
    return f"{name} + {format_number(100 * dec)}%"


# def format_percent(dec: float) -> str:
#     return f"{format_value(100 * dec)}%"


# def display_value(name: str, value: float) -> str:
#     return f"{name} {value}"


# def display_percent(name: str, dec: float):
#     return f"{name} {format_percent(dec)}"


# def display_percent_bonus(name: str, dec: float):
#     return f"{name} + {format_percent(dec)}"


# def format_absolute(name: str, value: float):
#     return f"{name} {format_value(value)}"


# def format_percent(name: str, value: float):
#     return f"{name} {format_value(100 * value)}%"


# def format_plus_percent(name: str, value: float):
#     return f"{name} + {format_value(100 * value)}%"


# def format_accuracy_cost(value: float) -> str:
#     return format_percent("Accuracy Cost", value)


# def format_accuracy_bonus(value: float) -> str:
#     if value == 0:
#         return ""
#     fstr = f"Accuracy + {truncate(value * 100)}%"
#     return fstr


# def format_damage_bonus(value: float) -> str:
#     if value == 0:
#         return ""
#     fstr = f"Damage + {truncate(value * 100)}%"
#     return fstr


# def format_damage_reduction(value: float) -> str:
#     if value == 0:
#         return ""
#     fstr = f"Damage Protection + {truncate(value * 100)}%"
#     return fstr


# def format_duration(value: int | float) -> str:
#     fstr = f"Duration {truncate(value)} sec"
#     return fstr


# def format_hardening(value: float) -> str:
#     if value == 0:
#         return ""
#     fstr = f"Hardening + {truncate(value * 100)}%"
#     return fstr


# def format_health_bonus(value: float) -> str:
#     if value == 0:
#         return ""
#     fstr = f"Health + {truncate(value * 100)}%"
#     return fstr


# def format_percent_dps(value: float):
#     fstr = f"Damage {truncate(value * 100)}% DPS"
#     return fstr


# def format_radius(value: int | float) -> str:
#     fstr = f"Radius {truncate(value)}m"
#     return fstr


# def format_recharge(seconds: int | float) -> str:
#     fstr = f"Recharge {truncate(seconds)} sec"
#     return fstr


def summarize(title: str, *desc: str, indent: int = 4) -> str:
    return "\n".join([title] + [f"{' ' * indent}{d}" for d in desc if d])


def summarize_Adrenaline_Burst(talents: Iterable[Talent]) -> str:

    level = get_ability_rank(talents, Ability.ADRENALINE_BURST)
    if level == 0:
        return ""

    # Base values
    recharge = {1: 120, 2: 90, 3: 45}[level]
    accuracy_cost = 0.30
    # Bonuses
    haste = 0
    # Apply spec
    if specialized := get_unlocked(talents, Specialization.ADRENALINE_BURST):
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

    level = get_ability_rank(talents, Ability.AI_HACKING)
    if level == 0:
        return ""

    # Base values
    duration = {1: 20, 2: 25, 3: 30}[level]
    recharge = {1: 60, 2: 50, 3: 40}[level]
    accuracy_cost = 0.80
    # Bonuses
    duration_bonus = get_bonus_sum(talents, (PercentBonus.ALL_DURATIONS, ))
    haste = get_bonus_sum(talents, (PercentBonus.AI_HACKING_HASTE, ))
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

    level = get_ability_rank(talents, Ability.ASSASSINATION)
    if level == 0:
        return ""

    # Base values
    percent_dps = {1: 2.00, 2: 2.50, 3: 3.00}[level]
    duration = 6
    recharge = 45
    # Bonuses
    haste = 0
    # Apply spec
    if specialized := get_unlocked(talents, Specialization.ASSASSINATION):
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
    accuracy_bonus = get_bonus_sum(talents, (PercentBonus.ASSAULT_RIFLE_ACCURACY, ))
    damage_bonus = get_bonus_sum(talents, (PercentBonus.ASSAULT_RIFLE_DAMAGE, PercentBonus.ALL_DAMAGE))
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

    level = get_ability_rank(talents, Ability.BARRIER)
    if level == 0:
        return ""
    
    # Base values
    duration = get_highest_value(talents, BaseValue.BARRIER_DURATION)
    shielding = get_highest_value(talents, BaseValue.BARRIER_SHIELDING)
    recharge = {1: 60, 2: 50, 3: 40}[level]
    acc_cost = 0.80
    regen = 0
    # Bonuses
    duration_bonus = get_bonus_sum(talents, (PercentBonus.BARRIER_DURATION, PercentBonus.ALL_DURATIONS))
    haste = get_bonus_sum(talents, (PercentBonus.BARRIER_HASTE, ))
    shielding_bonus = 0
    # Apply spec
    if specialized := get_unlocked(talents, Specialization.BARRIER):
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

    level = get_ability_rank(talents, Ability.CARNAGE)
    if level == 0:
        return ""

    # Base values
    percent_dps = {1: 2.00, 2: 2.25, 3: 2.50}[level]
    radius = {1: 2, 2: 2.5, 3: 3}[level]
    duration = 6
    recharge = 45
    # Bonuses
    duration_bonus = get_bonus_sum(talents, (PercentBonus.ALL_DURATIONS, ))
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

    level = get_ability_rank(talents, Ability.DAMPING)
    if level == 0:
        return ""

    # Base values
    radius = {1: 6, 2: 8, 3: 10}[level]
    recharge = {1: 60, 2: 50, 3: 40}[level]
    tech_mine_damage = {1: 50, 2: 100, 3: 100}[level]
    accuracy_cost = 0.60
    stun_duration = 3
    # Bonuses
    haste = get_bonus_sum(talents, (PercentBonus.DAMPING_HASTE, ))
    radius_bonus = get_bonus_sum(talents, (PercentBonus.DAMPING_RADIUS, ))
    stun_bonus = get_bonus_sum(talents, (PercentBonus.ALL_DURATIONS, ))
    tmd_bonus = get_bonus_sum(talents, (PercentBonus.TECH_MINE_DAMAGE, PercentBonus.ALL_DAMAGE))
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
    healing_bonus = get_bonus_sum(talents, (PercentBonus.FIRST_AID_HEALING, ))  # absolute value, not percent
    haste = get_bonus_sum(talents, (PercentBonus.FIRST_AID_HASTE, ))
    # Apply spec
    if specialized := get_unlocked(talents, Specialization.FIRST_AID):
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
    damage_reduction = get_bonus_sum(talents, (PercentBonus.HEAVY_ARMOR_DR, ))
    hardening = get_bonus_sum(talents, (PercentBonus.HEAVY_ARMOR_HARDENING, ))
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

    level = get_ability_rank(talents, Ability.IMMUNITY)
    if level == 0:
        return ""

    # Base values
    damage_reduction_mult = {1: 0.75, 2: 0.85, 3: 0.90}[level]
    duration = 6
    recharge = 45
    # Bonuses
    duration_bonus = get_bonus_sum(talents, (PercentBonus.ALL_DURATIONS, ))
    haste = 0
    # Apply spec
    if specialized := get_unlocked(talents, Specialization.IMMUNITY):
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

    level = get_ability_rank(talents, Ability.LIFT)
    if level == 0:
        return ""

    # Base values
    duration = get_highest_value(talents, BaseValue.LIFT_DURATION)
    accuracy_cost = {1: 0.80, 2: 0.60, 3: 0.40}[level]
    radius = {1: 4, 2: 5, 3: 6}[level]
    recharge = {1: 60, 2: 50, 3: 40}[level]
    # Bonuses
    duration_bonus = get_bonus_sum(talents, (PercentBonus.LIFT_DURATION, PercentBonus.ALL_DURATIONS))
    haste = get_bonus_sum(talents, (PercentBonus.LIFT_HASTE, ))
    radius_bonus = 0  # absolute
    # Apply spec
    if specialized := get_unlocked(talents, Specialization.LIFT):
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
    damage_reduction = get_bonus_sum(talents, (PercentBonus.LIGHT_ARMOR_DR, ))
    hardening = get_bonus_sum(talents, (PercentBonus.LIGHT_ARMOR_HARDENING, ))
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
    repair = get_bonus_sum(talents, (PercentBonus.HULL_REPAIR, ))
    # Don't bother if no bonuses
    if repair == 0:
        return ""

    summary = summarize(
        "Mako",
        f"Mako Hull Repair + {repair}",
    )
    return summary


def summarize_Marksman(talents: Iterable[Talent]) -> str:

    level = get_ability_rank(talents, Ability.MARKSMAN)
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
    if specialized := get_unlocked(talents, Specialization.ASSASSINATION):
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
    damage_reduction = get_bonus_sum(talents, (PercentBonus.MED_ARMOR_DR, ))
    hardening = get_bonus_sum(talents, (PercentBonus.MED_ARMOR_HARDENING, ))
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

    level = get_ability_rank(talents, Ability.NEURAL_SHOCK)
    if level == 0:
        return ""

    # Base values
    knockout = {1: 1, 2: 3, 3: 5}[level]
    toxic_damage = {1: 40, 2: 80, 3: 120}[level]
    acc_cost = 0.60
    recharge = 45
    # Bonuses
    haste = get_bonus_sum(talents, (PercentBonus.NEURAL_SHOCK_HASTE, ))
    knockout_bonus = get_bonus_sum(talents, (PercentBonus.ALL_DURATIONS, ))
    td_pct_bonus = get_bonus_sum(talents, (PercentBonus.ALL_DAMAGE, ))
    td_abs_bonus = 0
    # Apply spec
    if specialized := get_unlocked(talents, Specialization.NEURAL_SHOCK):
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

    level = get_ability_rank(talents, Ability.OVERKILL)
    if level == 0:
        return ""

    # Base values
    cooling = {1: 0.80, 2: 0.90, 3: 1.00}[level]
    damage = {1: 0.50, 2: 0.75, 3: 1.00}[level]
    duration = 6
    recharge = 45
    # Bonuses
    duration_bonus = get_bonus_sum(talents, (PercentBonus.ALL_DURATIONS, ))
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

    level = get_ability_rank(talents, Ability.OVERLOAD)
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
    duration_bonus = get_bonus_sum(talents, (PercentBonus.ALL_DURATIONS, ))
    haste = get_bonus_sum(talents, (PercentBonus.OVERLOAD_HASTE, ))
    radius_abs_bonus = 0
    radius_pct_bonus = get_bonus_sum(talents, (PercentBonus.OVERLOAD_RADIUS, ))
    shd_abs_bonus = 0
    shd_pct_bonus = get_bonus_sum(talents, (PercentBonus.ALL_DAMAGE, ))
    sunder_flat_bonus = 0
    tmd_abs_bonus = 0
    tmd_pct_bonus = get_bonus_sum(talents, (PercentBonus.TECH_MINE_DAMAGE, PercentBonus.ALL_DAMAGE))
    # Apply spec
    if specialized := get_unlocked(talents, Specialization.OVERLOAD):
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
    accuracy_bonus = get_bonus_sum(talents, (PercentBonus.PISTOL_ACCURACY, ))
    cooling = get_bonus_sum(talents, (PercentBonus.PISTOL_COOLING, ))
    damage = get_bonus_sum(talents, (PercentBonus.PISTOL_DAMAGE, PercentBonus.ALL_DAMAGE))
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

    level = get_ability_rank(talents, Ability.SABOTAGE)
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
    dps_pct_bonus = get_bonus_sum(talents, (PercentBonus.ALL_DAMAGE))
    duration_abs_bonus = 0
    duration_pct_bonus = get_bonus_sum(talents, (PercentBonus.ALL_DURATIONS, ))
    radius_abs_bonus = 0
    radius_pct_bonus = get_bonus_sum(talents, (PercentBonus.SABOTAGE_RADIUS, ))
    haste = get_bonus_sum(talents, (PercentBonus.SABOTAGE_HASTE, ))
    tmd_abs_bonus = 0
    tmd_pct_bonus = get_bonus_sum(talents, (PercentBonus.TECH_MINE_DAMAGE, PercentBonus.ALL_DAMAGE))
    # Apply spec
    if specialized := get_unlocked(talents, Specialization.SABOTAGE):
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
    acc_regen = get_bonus_sum(talents, (PercentBonus.ACCURACY_REGEN, ))
    bio_prot = get_bonus_sum(talents, (PercentBonus.BIOTIC_PROTECTION, ))
    health_regen = get_bonus_sum(talents, (PercentBonus.HEALTH_REGEN, ))
    hp = get_bonus_sum(talents, (PercentBonus.HEALTH, ))
    max_acc = get_bonus_sum(talents, (PercentBonus.MAX_ACCURACY, ))
    melee = get_bonus_sum(talents, (PercentBonus.MELEE_DAMAGE, PercentBonus.ALL_DAMAGE))
    shields = get_bonus_sum(talents, (PercentBonus.SHIELD_CAPACITY, ))
    tech_prot = get_bonus_sum(talents, (PercentBonus.TECH_PROTECTION, ))
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

    level = get_ability_rank(talents, Ability.SHIELD_BOOST)
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

    # Bonuses
    damage_bonus = get_bonus_sum(talents, (PercentBonus.SHOTGUN_DAMAGE, PercentBonus.ALL_DAMAGE))
    accuracy_bonus = get_bonus_sum(talents, (PercentBonus.SHOTGUN_ACCURACY, ))
    # Don't bother if no bonuses
    if damage_bonus == accuracy_bonus == 0:
        return ""

    summary = summarize(
        "Shotgun",
        format_damage_bonus(truncate(damage_bonus)),
        format_accuracy_bonus(truncate(accuracy_bonus))
    )
    return summary


def summarize_Singularity(talents: Iterable[Talent]) -> str:

    level = get_ability_rank(talents, Ability.SINGULARITY)
    if level == 0:
        return ""

    # Base values
    radius = get_highest_value(talents, BaseValue.SINGULARITY_RADIUS)
    duration = {1: 4, 2: 6, 3: 8}[level]
    recharge = {1: 60, 2: 50, 3: 40}[level]
    acc_cost = 0.80
    # Bonuses
    duration_bonus = get_bonus_sum(talents, (PercentBonus.SINGULARITY_DURATION, ))
    haste = get_bonus_sum(talents, (PercentBonus.SINGULARITY_HASTE, ))
    # Apply bonuses
    duration *= (1.00 + duration_bonus)
    recharge *= (1.00 - haste)

    summary = summarize(
        format_title("Singularity", level),
        format_radius(radius),
        format_duration(duration),
        format_recharge(recharge),
        format_accuracy_cost(acc_cost),
    )
    return summary


def summarize_Sniper_Rifles(talents: Iterable[Talent]) -> str:

    # Bonuses
    damage_bonus = get_bonus_sum(talents, (PercentBonus.SNIPER_RIFLE_DAMAGE, PercentBonus.ALL_DAMAGE))
    accuracy_bonus = get_bonus_sum(talents, (PercentBonus.SNIPER_RIFLE_ACCURACY, ))
    cooling = get_bonus_sum(talents, (PercentBonus.SNIPER_RIFLE_COOLING, ))
    # Don't bother if no bonuses
    if damage_bonus == accuracy_bonus == cooling == 0:
        return ""

    summary = summarize(
        "Sniper Rifles",
        format_damage_bonus(damage_bonus),
        format_accuracy_bonus(accuracy_bonus),
        f"Cooling + {truncate(cooling * 100)}%" if cooling else "",
    )
    return summary


def summarize_Stasis(talents: Iterable[Talent]) -> str:

    level = get_ability_rank(talents, Ability.STASIS)
    if level == 0:
        return ""

    # Base values
    duration = get_highest_value(talents, BaseValue.STASIS_DURATION)
    recharge = {1: 60, 2: 50, 3: 40}[level]
    acc_cost = 0.80
    # Bonuses
    duration_bonus = get_bonus_sum(talents, (PercentBonus.STASIS_DURATION, PercentBonus.ALL_DURATIONS))
    haste = get_bonus_sum(talents, (PercentBonus.STASIS_HASTE, ))
    # Spec
    specialized = get_unlocked(talents, Specialization.STASIS)
    # Apply bonuses
    duration *= (1.00 + duration_bonus)
    recharge *= (1.00 - haste)

    summary = summarize(
        format_title("Stasis", level),
        "Stasis Specialization:" if specialized else "",
        "    Damage enemies in Stasis" if specialized else "",
        format_duration(duration),
        format_recharge(recharge),
        format_accuracy_cost(acc_cost),
    )
    return summary


def summarize_Throw(talents: Iterable[Talent]) -> str:

    level = get_ability_rank(talents, Ability.THROW)
    if level == 0:
        return ""

    # Base values
    force = get_highest_value(talents, BaseValue.THROW_FORCE)
    acc_cost = {1: 0.60, 2: 0.45, 3: 0.30}[level]
    radius = {1: 4, 2: 5, 3: 6}[level]
    recharge = {1: 60, 2: 50, 3: 40}[level]
    # Bonuses
    damage = get_bonus_sum(talents, (PercentBonus.THROW_DAMAGE, PercentBonus.ALL_DAMAGE))
    force_bonus = get_bonus_sum(talents, ( PercentBonus.THROW_FORCE, ))
    haste = get_bonus_sum(talents, (PercentBonus.THROW_HASTE, ))
    # Apply bonuses
    force *= (1.00 + force_bonus)
    recharge *= (1.00 - haste)

    summary = summarize(
        format_title("Throw", level),
        f"Force {truncate(force)}N",
        format_damage_bonus(damage),
        format_radius(radius),
        format_recharge(recharge),
        format_accuracy_cost(acc_cost),
    )
    return summary


def summarize_Unity(talents: Iterable[Talent]) -> str:

    level = get_ability_rank(talents, Ability.UNITY)
    if level == 0:
        return ""

    health = {1: 0.15, 2: 0.20, 3: 0.30}[level]
    shields = {1: 0.40, 2: 0.60, 3: 1.00}[level]
    recharge = {1: 150, 2: 120, 3: 90}[level]
    acc_cost = 0.45

    summary = summarize(
        format_title("Unity", level),
        f"Health {truncate(health * 100)}%",
        f"Shields {truncate(shields * 100)}%",
        format_recharge(recharge),
        format_accuracy_cost(acc_cost),
    )
    return summary


def summarize_Warp(talents: Iterable[Talent]) -> str:

    level = get_ability_rank(talents, Ability.WARP)
    if level == 0:
        return ""

    # Base values
    duration = get_highest_value(talents, BaseValue.WARP_DURATION)
    dps = {1: 6, 2: 8, 3: 10}[level]
    radius = {1: 4, 2: 5, 3: 6}[level]
    recharge = {1: 60, 2: 50, 3: 40}[level]
    sunder = {1: 0.50, 2: 0.60, 3: 0.75}[level]
    acc_cost = 0.80
    # Bonuses
    dps_bonus = get_bonus_sum(talents, (PercentBonus.ALL_DAMAGE, ))
    duration_bonus = get_bonus_sum(talents, (PercentBonus.WARP_DURATION, PercentBonus.ALL_DURATIONS))
    haste = get_bonus_sum(talents, (PercentBonus.WARP_HASTE, ))
    radius_abs_bonus = 0
    # Apply spec
    if specialized := get_unlocked(talents, Specialization.WARP):
        radius_abs_bonus += 2
        dps_bonus += 0.25
    # Apply bonuses
    dps *= (1 + dps_bonus)
    duration *= (1 + duration_bonus)
    radius += radius_abs_bonus
    recharge *= (1.00 - haste)

    summary = summarize(
        format_title("Warp", level),
        "Warp Specialization" if specialized else "",
        f"DPS {dps}",
        f"Reduce Damage Protection {truncate(sunder * 100)}%",
        format_radius(radius),
        format_duration(duration),
        format_recharge(recharge),
        format_accuracy_cost(acc_cost),
    )
    return summary
