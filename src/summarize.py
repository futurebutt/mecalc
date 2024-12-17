from collections.abc import Iterable

from enums import AbilityLevel, AbilitySpec, Modifier
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


def get_ability_specialization(talents: Iterable[Talent], dependency: AbilitySpec) -> bool:
    for talent in talents:
        abilities = talent.get_abilities()
        if abilities.get(dependency, False):
            return True
    else:
        return False


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
    accuracy_cost = 0.30

    summary = summarize(
        format_ability_title(title, level),
        format_recharge(recharge),
        format_accuracy_cost(accuracy_cost),
    )
    return summary


def summarize_AI_Hacking(talents: Iterable[Talent]) -> str:

    level = get_ability_level(talents, AbilityLevel.AI_HACKING)
    if level == 0:
        return ""

    title = "AI Hacking"
    duration = {1: 20, 2: 25, 3: 30}[level]
    recharge = {1: 60, 2: 50, 3: 40}[level]
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

    if specialized := get_ability_specialization(talents, AbilitySpec.ASSASSINATION):
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
    damage = calculate_bonus(talents, (Modifier.ASSAULT_RIFLE_DAMAGE, Modifier.WEAPON_DAMAGE))
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
    duration = calculate_bonus(talents, (Modifier.BARRIER_DURATION, ))
    strength = calculate_bonus(talents, (Modifier.BARRIER_SHIELDING, ))
    assert duration and strength, "should never happen if level is not zero"

    recharge = {1: 60, 2: 50, 3: 40}[level]
    acc_cost = 0.80

    summary = summarize(
        format_ability_title(title, level),
        f"Shielding {strength}",
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
    duration = 6
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
    tech_mine_damage *= (1 + calculate_bonus(talents, (Modifier.TECH_MINE_DAMAGE, )))
    stun_duration = 3
    radius = {1: 6, 2: 8, 3: 10}[level]
    radius *= (1 + calculate_bonus(talents, (Modifier.TECH_MINE_RADIUS, )))
    recharge = {1: 60, 2: 50, 3: 40}[level]
    recharge *= (1 - calculate_bonus(talents, (Modifier.TECH_MINE_HASTE, )))
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
    recharge = 20

    summary = summarize(
        title,
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
    duration = 6
    recharge = 45

    if specialized := get_ability_specialization(talents, AbilitySpec.IMMUNITY):
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

    duration = calculate_bonus(talents, (Modifier.LIFT_DURATION, ))

    radius = {1: 4, 2: 5, 3: 6}[level]
    recharge = {1: 60, 2: 50, 3: 40}[level]
    acc_cost = {1: 0.80, 2: 0.60, 3: 0.40}[level]

    summary = summarize(
        format_ability_title(title, level),
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

    if specialized := get_ability_specialization(talents, AbilitySpec.ASSASSINATION):
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
    toxic_damage = {1: 40, 2: 80, 3: 120}[level]
    knockout = {1: 1, 2: 3, 3: 5}[level]
    recharge = 45
    acc_cost = 0.60

    summary = summarize(
        format_ability_title(title, level),
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
    heat_reduction = {1: 0.80, 2: 0.90, 3: 1.00}[level]
    damage = {1: 0.50, 2: 0.75, 3: 1.00}[level]
    duration = 6
    recharge = 45

    summary = summarize(
        format_ability_title(title, level),
        f"Reduced Heat {truncate(heat_reduction * 100)}%",
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
    tech_mine_damage = {1: 50, 2: 100, 3: 150}[level]
    tech_mine_damage *= (1 + calculate_bonus(talents, (Modifier.TECH_MINE_DAMAGE, )))
    shield_damage = {1: 200, 2: 400, 3: 600}[level]
    radius = {1: 6, 2: 8, 3: 10}[level]
    radius *= (1 + calculate_bonus(talents, (Modifier.TECH_MINE_RADIUS, )))
    sunder = {1: 0.20, 2: 0.25, 3: 0.30}[level]
    duration = 10
    recharge = {1: 60, 2: 50, 3: 40}[level]
    recharge *= (1 - calculate_bonus(talents, (Modifier.TECH_MINE_HASTE, )))
    accuracy_cost = 0.60

    summary = summarize(
        format_ability_title(title, level),
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
    damage = calculate_bonus(talents, (Modifier.PISTOL_DAMAGE, Modifier.WEAPON_DAMAGE))
    accuracy = calculate_bonus(talents, (Modifier.PISTOL_ACCURACY, ))
    if damage == accuracy == 0:
        return ""

    summary = summarize(
        title,
        format_damage_bonus(damage),
        format_accuracy_bonus(accuracy)
    )
    return summary


def summarize_Sabotage(talents: Iterable[Talent]) -> str:

    level = get_ability_level(talents, AbilityLevel.SABOTAGE)
    if level == 0:
        return ""

    title = "Sabotage"
    tech_mine_damage = {1: 50, 2: 100, 3: 150}[level]
    tech_mine_damage *= (1 + calculate_bonus(talents, (Modifier.TECH_MINE_DAMAGE, )))
    radius = {1: 6, 2: 8, 3: 10}[level]
    radius *= (1 + calculate_bonus(talents, (Modifier.TECH_MINE_RADIUS, )))
    burn_dps = {1: 2, 2: 3, 3: 4}[level]
    duration = {1: 15, 2: 20, 3: 25}[level]
    recharge = {1: 60, 2: 50, 3: 40}[level]
    recharge *= (1 - calculate_bonus(talents, (Modifier.TECH_MINE_HASTE, )))
    accuracy_cost = 0.60

    summary = summarize(
        format_ability_title(title, level),
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
    health_regen = calculate_bonus(talents, (Modifier.HEALTH_REGEN, ))
    melee = calculate_bonus(talents, (Modifier.MELEE_DAMAGE, ))
    shields = calculate_bonus(talents, (Modifier.SHIELD_CAPACITY, ))
    if hp == melee == health_regen == shields == 0:
        return ""

    summary = summarize(
        title,
        format_health_bonus(hp),
        f"Shields + {truncate(shields)}",
        f"Health Regen {truncate(health_regen)} per sec" if health_regen else "",
        f"Melee Damage + {truncate(melee * 100)}%" if melee else "",
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
    damage = calculate_bonus(talents, (Modifier.SHOTGUN_DAMAGE, Modifier.WEAPON_DAMAGE))
    accuracy = calculate_bonus(talents, (Modifier.SHOTGUN_ACCURACY, ))
    if damage == accuracy == 0:
        return ""

    summary = summarize(
        title,
        format_damage_bonus(damage),
        format_accuracy_bonus(accuracy)
    )
    return summary


def summarize_Singularity(talents: Iterable[Talent]) -> str:

    level = get_ability_level(talents, AbilityLevel.SINGULARITY)
    if level == 0:
        return ""

    title = "Singularity"

    radius = calculate_bonus(talents, (Modifier.SINGULARITY_RADIUS, ))

    duration = {1: 4, 2: 6, 3: 8}[level]
    recharge = {1: 60, 2: 50, 3: 40}[level]

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

    title = "Sniper Rifle"
    damage = calculate_bonus(talents, (Modifier.SNIPER_RIFLE_DAMAGE, Modifier.WEAPON_DAMAGE))
    accuracy = calculate_bonus(talents, (Modifier.SNIPER_RIFLE_ACCURACY, ))
    if damage == accuracy == 0:
        return ""

    summary = summarize(
        title,
        format_damage_bonus(damage),
        format_accuracy_bonus(accuracy)
    )
    return summary


def summarize_Stasis(talents: Iterable[Talent]) -> str:

    level = get_ability_level(talents, AbilityLevel.STASIS)
    if level == 0:
        return ""

    title = "Stasis"

    duration = calculate_bonus(talents, (Modifier.STASIS_DURATION, ))

    recharge = {1: 60, 2: 50, 3: 40}[level]

    acc_cost = 0.80

    summary = summarize(
        format_ability_title(title, level),
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

    force = calculate_bonus(talents, (Modifier.THROW_FORCE, ))

    radius = {1: 4, 2: 5, 3: 6}[level]
    recharge = {1: 60, 2: 50, 3: 40}[level]
    acc_cost = {1: 0.60, 2: 0.45, 3: 0.30}[level]

    summary = summarize(
        format_ability_title(title, level),
        f"Force {force}N",
        format_radius(radius),
        format_recharge(recharge),
        format_accuracy_cost(acc_cost),
    )
    return summary


def summarize_Warp(talents: Iterable[Talent]) -> str:

    level = get_ability_level(talents, AbilityLevel.WARP)
    if level == 0:
        return ""

    title = "Warp"

    duration = calculate_bonus(talents, (Modifier.WARP_DURATION, ))

    dps = {1: 6, 2: 8, 3: 10}[level]
    sunder = {1: 0.50, 2: 0.60, 3: 0.75}[level]
    radius = {1: 4, 2: 5, 3: 6}[level]
    recharge = {1: 60, 2: 50, 3: 40}[level]

    acc_cost = 0.80

    summary = summarize(
        format_ability_title(title, level),
        f"DPS {dps}",
        f"Reduce Damage Protection {truncate(sunder * 100)}%",
        format_radius(radius),
        format_duration(duration),
        format_recharge(recharge),
        format_accuracy_cost(acc_cost),
    )
    return summary
