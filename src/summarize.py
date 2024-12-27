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


def format_ability_title(name: str, level: int) -> str:
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

    title = "Adrenaline Burst"

    recharge = {1: 120, 2: 90, 3: 45}[level]
    if specialized := get_ability_specialization(talents, Specialization.ADRENALINE_BURST):
        recharge *= (1 - 0.25)

    accuracy_cost = 0.30

    summary = summarize(
        format_ability_title(title, level),
        "Adrenaline Burst Specialization" if specialized else "",
        format_recharge(recharge),
        format_accuracy_cost(accuracy_cost),
    )
    return summary


def summarize_AI_Hacking(talents: Iterable[Talent]) -> str:

    level = get_ability_level(talents, AbilityLevel.AI_HACKING)
    if level == 0:
        return ""

    title = "AI Hacking"

    haste = calculate_bonus(talents, (Modifier.AI_HACKING_HASTE, ))
    duration_bonus = calculate_bonus(talents, (Modifier.ALL_DURATION, ))

    duration = {1: 20, 2: 25, 3: 30}[level] * (1 + duration_bonus)
    recharge = {1: 60, 2: 50, 3: 40}[level]
    recharge *= (1.00 - haste)

    accuracy_cost = 0.80

    summary = summarize(
        format_ability_title(title, level),
        format_duration(duration),
        format_recharge(recharge),
        format_accuracy_cost(accuracy_cost),
    )
    return summary


def summarize_Assassination(talents: Iterable[Talent]) -> str:

    level = get_ability_level(talents, AbilityLevel.ASSASSINATION)
    if level == 0:
        return ""

    title = "Assassination"
    percent_dps = {1: 2.00, 2: 2.50, 3: 3.00}[level]
    duration = 6
    recharge = 45

    if specialized := get_ability_specialization(talents, Specialization.ASSASSINATION):
        recharge *= (1 - 0.25)

    summary = summarize(
        format_ability_title(title, level),
        "Assassination Specialization" if specialized else "",
        format_percent_dps(percent_dps),
        format_duration(duration),
        format_recharge(recharge),
    )
    return summary


def summarize_Assault_Rifle(talents: Iterable[Talent]) -> str:

    title = "Assault Rifles"
    damage = calculate_bonus(talents, (Modifier.ASSAULT_RIFLE_DAMAGE, Modifier.ALL_DAMAGE))
    accuracy = calculate_bonus(talents, (Modifier.ASSAULT_RIFLE_ACCURACY, ))
    if damage == accuracy == 0:
        return ""

    summary = summarize(
        title,
        format_damage_bonus(damage),
        format_accuracy_bonus(accuracy)
    )
    return summary


def summarize_Barrier(talents: Iterable[Talent]) -> str:

    level = get_ability_level(talents, AbilityLevel.BARRIER)
    if level == 0:
        return ""

    title = "Barrier"

    duration = get_highest_value(talents, BaseValue.BARRIER_DURATION)
    duration_bonus = calculate_bonus(talents, (Modifier.BARRIER_DURATION, Modifier.ALL_DURATION))
    strength = calculate_bonus(talents, (Modifier.BARRIER_SHIELDING, ))
    strength_bonus = 0
    haste = calculate_bonus(talents, (Modifier.BARRIER_HASTE, ))

    recharge = {1: 60, 2: 50, 3: 40}[level]

    acc_cost = 0.80
    regen = 0

    if specialized := get_ability_specialization(talents, Specialization.BARRIER):
        duration_bonus += 0.25
        strength_bonus += 0.25
        regen = 40

    duration *= (1.00 + duration_bonus)
    strength *= (1.00 + strength_bonus)
    recharge *= (1.00 - haste)

    summary = summarize(
        format_ability_title(title, level),
        "Barrier Specialization" if specialized else "",
        f"Shielding {strength}",
        f"Regen {regen} pts / sec" if regen else "",
        format_duration(duration),
        format_recharge(recharge),
        format_accuracy_cost(acc_cost),
    )
    return summary


def summarize_Carnage(talents: Iterable[Talent]) -> str:

    rank = get_ability_level(talents, AbilityLevel.CARNAGE)
    if rank == 0:
        return ""

    title = "Carnage"
    percent_dps = {1: 2.00, 2: 2.25, 3: 2.50}[rank]
    radius = {1: 2, 2: 2.5, 3: 3}[rank]
    duration = 6 + calculate_bonus(talents, (Modifier.ALL_DURATION, ))
    recharge = 45

    summary = summarize(
        format_ability_title(title, rank),
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

    title = "Damping"
    tech_mine_damage = {1: 50, 2: 100, 3: 100}[level]
    tech_mine_damage *= (1 + calculate_bonus(talents, (Modifier.TECH_MINE_DAMAGE, Modifier.ALL_DAMAGE)))
    stun_duration = 3 * (1 + calculate_bonus(talents, (Modifier.ALL_DURATION, )))
    radius = {1: 6, 2: 8, 3: 10}[level]
    radius *= (1 + calculate_bonus(talents, (Modifier.DAMPING_RADIUS, )))
    recharge = {1: 60, 2: 50, 3: 40}[level]
    haste = calculate_bonus(talents, (Modifier.DAMPING_HASTE, ))
    recharge *= (1.00 - haste)
    accuracy_cost = 0.60

    summary = summarize(
        format_ability_title(title, level),
        f"Tech Mine Damage {truncate(tech_mine_damage)}",
        f"Stun {stun_duration} sec",
        format_radius(radius),
        format_recharge(recharge),
        format_accuracy_cost(accuracy_cost),
    )
    return summary


def summarize_First_Aid(talents: Iterable[Talent]) -> str:

    title = "First Aid"
    # 40 = base heal
    healing = 40 + calculate_bonus(talents, (Modifier.FIRST_AID_HEALING, ))
    haste = calculate_bonus(talents, (Modifier.FIRST_AID_HASTE, ))
    recharge = 20 * (1.00 - haste)

    if specialized := get_ability_specialization(talents, Specialization.FIRST_AID):
        healing += 80

    summary = summarize(
        title,
        "First Aid Specialization:" if specialized else "",
        "    Ignore toxic damage" if specialized else "",
        "    Revive fallen party members" if specialized else "",
        f"Health Restored {truncate(healing)}",
        format_recharge(recharge),
    )
    return summary


def summarize_Heavy_Armor(talents: Iterable[Talent]) -> str:

    title = "Heavy Armor"
    damage_reduction = calculate_bonus(talents, (Modifier.HEAVY_ARMOR_DR, ))
    hardening = calculate_bonus(talents, (Modifier.HEAVY_ARMOR_HARDENING, ))
    if damage_reduction == hardening == 0:
        return ""

    summary = summarize(
        title,
        format_damage_reduction(damage_reduction),
        format_hardening(hardening),
    )
    return summary


def summarize_Immunity(talents: Iterable[Talent]) -> str:

    level = get_ability_level(talents, AbilityLevel.IMMUNITY)
    if level == 0:
        return ""

    title = "Immunity"
    damage_reduction_mult = {1: 0.75, 2: 0.85, 3: 0.90}[level]
    duration = 6 * (1 + calculate_bonus(talents, (Modifier.ALL_DURATION, )))
    recharge = 45

    if specialized := get_ability_specialization(talents, Specialization.IMMUNITY):
        recharge *= (1 - 0.25)

    summary = summarize(
        format_ability_title(title, level),
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

    title = "Lift"

    # TODO: This highlights need to distinguish ability base values from bonuses:
    # ----
    duration = get_highest_value(talents, BaseValue.LIFT_DURATION)
    duration_bonus = calculate_bonus(talents, (Modifier.LIFT_DURATION, Modifier.ALL_DURATION))
    duration *= (1.00 + duration_bonus)
    # ----
    haste = calculate_bonus(talents, (Modifier.LIFT_HASTE, ))

    radius = {1: 4, 2: 5, 3: 6}[level]
    recharge = {1: 60, 2: 50, 3: 40}[level]
    recharge *= (1.00 - haste)
    acc_cost = {1: 0.80, 2: 0.60, 3: 0.40}[level]

    if specialized := get_ability_specialization(talents, Specialization.LIFT):
        radius += 4

    summary = summarize(
        format_ability_title(title, level),
        "Lift Specialization" if specialized else "",
        format_duration(duration),
        format_radius(radius),
        format_recharge(recharge),
        format_accuracy_cost(acc_cost),
    )
    return summary


def summarize_Light_Armor(talents: Iterable[Talent]) -> str:

    title = "Light Armor"
    damage_reduction = calculate_bonus(talents, (Modifier.LIGHT_ARMOR_DR, ))
    hardening = calculate_bonus(talents, (Modifier.LIGHT_ARMOR_HARDENING, ))
    if damage_reduction == hardening == 0:
        return ""

    summary = summarize(
        title,
        format_damage_reduction(damage_reduction),
        format_hardening(hardening),
    )
    return summary


def summarize_Mako(talents: Iterable[Talent]) -> str:

    title = "Mako"
    repair = calculate_bonus(talents, (Modifier.HULL_REPAIR, ))
    if repair == 0:
        return ""

    summary = summarize(
        title,
        f"Mako Hull Repair + {repair}",
    )
    return summary


def summarize_Marksman(talents: Iterable[Talent]) -> str:

    level = get_ability_level(talents, AbilityLevel.MARKSMAN)
    if level == 0:
        return ""

    title = "Marksman"
    accuracy = 0.60
    damage = {1: 0.25, 2: 0.50, 3: 0.75}[level]
    headshot_damage = {1: 0.50, 2: 0.75, 3: 1.00}[level]
    duration = 6
    recharge = 45

    if specialized := get_ability_specialization(talents, Specialization.ASSASSINATION):
        recharge *= (1 - 0.25)

    summary = summarize(
        format_ability_title(title, level),
        "Assassination Specialization" if specialized else "",
        format_accuracy_bonus(accuracy),
        format_damage_bonus(damage),
        f"Headshot Damage + {truncate(headshot_damage * 100)}%",
        format_duration(duration),
        format_recharge(recharge),
    )
    return summary


def summarize_Medium_Armor(talents: Iterable[Talent]) -> str:

    title = "Medium Armor"
    damage_reduction = calculate_bonus(talents, (Modifier.MED_ARMOR_DR, ))
    hardening = calculate_bonus(talents, (Modifier.MED_ARMOR_HARDENING, ))
    if damage_reduction == hardening == 0:
        return ""

    summary = summarize(
        title,
        format_damage_reduction(damage_reduction),
        format_hardening(hardening),
    )
    return summary


def summarize_Neural_Shock(talents: Iterable[Talent]) -> str:

    level = get_ability_level(talents, AbilityLevel.NEURAL_SHOCK)
    if level == 0:
        return ""

    title = "Neural Shock"

    haste = calculate_bonus(talents, (Modifier.NEURAL_SHOCK_HASTE, ))

    toxic_damage = {1: 40, 2: 80, 3: 120}[level]
    toxic_damage_bonus = calculate_bonus(talents, (Modifier.ALL_DAMAGE, ))
    knockout = {1: 1, 2: 3, 3: 5}[level]
    knockout_bonus = calculate_bonus(talents, (Modifier.ALL_DURATION, ))

    recharge = 45 * (1.00 - haste)
    acc_cost = 0.60

    if specialized := get_ability_specialization(talents, Specialization.NEURAL_SHOCK):
        toxic_damage += 40
        knockout_bonus += 0.25

    toxic_damage *= (1 + toxic_damage_bonus)
    knockout *= (1 + knockout_bonus)

    summary = summarize(
        format_ability_title(title, level),
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

    title = "Overkill"
    cooling = {1: 0.80, 2: 0.90, 3: 1.00}[level]
    damage = {1: 0.50, 2: 0.75, 3: 1.00}[level]
    duration = 6 * (1 + calculate_bonus(talents, (Modifier.ALL_DURATION, )))
    recharge = 45

    summary = summarize(
        format_ability_title(title, level),
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

    title = "Overload"

    tmd_bonus = calculate_bonus(talents, (Modifier.TECH_MINE_DAMAGE, Modifier.ALL_DAMAGE))
    sd_bonus = calculate_bonus(talents, (Modifier.ALL_DAMAGE, ))
    duration_bonus = calculate_bonus(talents, (Modifier.ALL_DURATION, ))
    radius_bonus = calculate_bonus(talents, (Modifier.OVERLOAD_RADIUS, ))
    haste = calculate_bonus(talents, (Modifier.OVERLOAD_HASTE, ))

    tech_mine_damage = {1: 50, 2: 100, 3: 150}[level]
    shield_damage = {1: 200, 2: 400, 3: 600}[level]
    radius = {1: 6, 2: 8, 3: 10}[level]
    sunder = {1: 0.20, 2: 0.25, 3: 0.30}[level]
    recharge = {1: 60, 2: 50, 3: 40}[level]

    duration = 10
    accuracy_cost = 0.60

    if specialized := get_ability_specialization(talents, Specialization.OVERLOAD):
        radius += 2
        tech_mine_damage += 50
        shield_damage += 200
        sunder += 0.05

    tech_mine_damage *= (1.00 + tmd_bonus)
    shield_damage *= (1.00 + sd_bonus)
    duration *= (1.00 + duration_bonus)
    radius *= (1.00 + radius_bonus)
    recharge *= (1.00 - haste)

    summary = summarize(
        format_ability_title(title, level),
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

    title = "Pistol"
    damage = calculate_bonus(talents, (Modifier.PISTOL_DAMAGE, Modifier.ALL_DAMAGE))
    accuracy = calculate_bonus(talents, (Modifier.PISTOL_ACCURACY, ))
    cooling = calculate_bonus(talents, (Modifier.PISTOL_COOLING, ))
    if damage == accuracy == cooling == 0:
        return ""

    summary = summarize(
        title,
        format_damage_bonus(truncate(damage)),
        format_accuracy_bonus(truncate(accuracy)),
        f"Cooling + {truncate(cooling * 100)}%" if cooling else "",
    )
    return summary


def summarize_Sabotage(talents: Iterable[Talent]) -> str:

    level = get_ability_level(talents, AbilityLevel.SABOTAGE)
    if level == 0:
        return ""

    title = "Sabotage"

    tmd_bonus = calculate_bonus(talents, (Modifier.TECH_MINE_DAMAGE, Modifier.ALL_DAMAGE))
    dps_bonus = calculate_bonus(talents, (Modifier.ALL_DAMAGE))
    radius_bonus = calculate_bonus(talents, (Modifier.SABOTAGE_RADIUS, ))
    duration_bonus = calculate_bonus(talents, (Modifier.ALL_DURATION, ))
    haste = calculate_bonus(talents, (Modifier.SABOTAGE_HASTE, ))

    tech_mine_damage = {1: 50, 2: 100, 3: 150}[level]
    radius = {1: 6, 2: 8, 3: 10}[level]
    burn_dps = {1: 2, 2: 3, 3: 4}[level]
    duration = {1: 15, 2: 20, 3: 25}[level]
    recharge = {1: 60, 2: 50, 3: 40}[level]

    accuracy_cost = 0.60

    if specialized := get_ability_specialization(talents, Specialization.SABOTAGE):
        radius += 2
        tech_mine_damage += 50
        burn_dps += 1
        duration += 5

    tech_mine_damage *= (1.00 + tmd_bonus)
    burn_dps *= (1.00 + dps_bonus)
    radius *= (1.00 + radius_bonus)
    duration *= (1.00 + duration_bonus)
    recharge *= (1.00 - haste)

    summary = summarize(
        format_ability_title(title, level),
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

    title = "Shepard"

    hp = calculate_bonus(talents, (Modifier.HEALTH, ))
    max_acc = calculate_bonus(talents, (Modifier.MAX_ACCURACY, ))
    acc_regen = calculate_bonus(talents, (Modifier.ACCURACY_REGEN, ))
    health_regen = calculate_bonus(talents, (Modifier.HEALTH_REGEN, ))
    melee = calculate_bonus(talents, (Modifier.MELEE_DAMAGE, Modifier.ALL_DAMAGE))
    shields = calculate_bonus(talents, (Modifier.SHIELD_CAPACITY, ))
    bio_prot = calculate_bonus(talents, (Modifier.BIOTIC_PROTECTION, ))
    tech_prot = calculate_bonus(talents, (Modifier.TECH_PROTECTION, ))

    if hp == melee == health_regen == shields == bio_prot == tech_prot == 0:
        return ""

    summary = summarize(
        title,
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

    title = "Shield Boost"
    shields_restored = {1: 0.30, 2: 0.40, 3: 0.50}[level]
    accuracy_cost = 0.30
    duration = 2
    recharge = 45

    summary = summarize(
        format_ability_title(title, level),
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
        format_ability_title(title, level),
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
    duration_bonus = calculate_bonus(talents, (Modifier.STASIS_DURATION, Modifier.ALL_DURATION))
    duration *= (1.00 + duration_bonus)
    haste = calculate_bonus(talents, (Modifier.STASIS_HASTE, ))

    recharge = {1: 60, 2: 50, 3: 40}[level]
    recharge *= (1.00 - haste)

    acc_cost = 0.80

    specialized = get_ability_specialization(talents, Specialization.STASIS)

    summary = summarize(
        format_ability_title(title, level),
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
        format_ability_title(title, level),
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
        format_ability_title(title, level),
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
    duration_bonus = calculate_bonus(talents, (Modifier.WARP_DURATION, Modifier.ALL_DURATION))
    haste = calculate_bonus(talents, (Modifier.WARP_HASTE, ))
    dps_bonus = calculate_bonus(talents, (Modifier.ALL_DAMAGE, ))

    if specialized := get_ability_specialization(talents, Specialization.WARP):
        radius += 2
        dps_bonus += 0.25

    dps *= (1 + dps_bonus)
    duration *= (1 + duration_bonus)
    recharge *= (1.00 - haste)

    summary = summarize(
        format_ability_title(title, level),
        "Warp Specialization" if specialized else "",
        f"DPS {dps}",
        f"Reduce Damage Protection {truncate(sunder * 100)}%",
        format_radius(radius),
        format_duration(duration),
        format_recharge(recharge),
        format_accuracy_cost(acc_cost),
    )
    return summary
