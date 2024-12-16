from collections.abc import Iterable

from enums import AbilityLevel, Modifier
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


def truncate(value: float) -> int | float:
    if value % 1 == 0:
        value = int(value)
    else:
        value = round(value, 3)
    return value


def format_ability_title(name: str, level: int) -> str:
    fstr = name + {1: "", 2: " (Advanced)", 3: " (Master)"}[level]
    return fstr


def format_accuracy_cost(value: float):
    fstr = f"Accuracy Cost {truncate(value * 100)}%"
    return fstr


def format_accuracy_bonus(value: float) -> str:
    fstr = f"Accuracy + {truncate(value * 100)}%"
    return fstr


def format_damage_bonus(value: float) -> str:
    fstr = f"Damage + {truncate(value * 100)}%"
    return fstr


def format_damage_reduction(value: float) -> str:
    fstr = f"Damage Protection + {truncate(value * 100)}%"
    return fstr


def format_duration(value: int | float) -> str:
    fstr = f"Duration {truncate(value)} sec"
    return fstr


def format_hardening(value: float) -> str:
    fstr = f"Hardening + {truncate(value * 100)}%"
    return fstr


def format_health_bonus(value: float) -> str:
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
    desc = [" "*indent + d for d in desc]
    summary = "\n".join([title] + desc)
    return summary


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


def summarize_Assassination(talents: Iterable[Talent]) -> str:

    level = get_ability_level(talents, AbilityLevel.ASSASSINATION)
    if level == 0:
        return ""

    title = "Assassination"
    percent_dps = {1: 2.00, 2: 2.50, 3: 3.00}[level]
    duration = 6
    recharge = 45

    summary = summarize(
        format_ability_title(title, level),
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


def summarize_First_Aid(talents: Iterable[Talent]) -> str:

    title = "First Aid"
    healing = calculate_bonus(talents, (Modifier.FIRST_AID_HEALING, ))
    if healing == 0:
        return ""
    
    summary = summarize(
        title,
        f"Health Restored + {healing}",
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

    summary = summarize(
        format_ability_title(title, level),
        f"Damage Reduction {truncate(damage_reduction_mult * 100)}%",
        format_duration(duration),
        format_recharge(recharge),
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

    summary = summarize(
        format_ability_title(title, level),
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


def summarize_Shepard(talents: Iterable[Talent]) -> str:

    title = "Shepard"
    hp = calculate_bonus(talents, (Modifier.HEALTH, ))
    melee = calculate_bonus(talents, (Modifier.MELEE_DAMAGE, ))
    if hp == melee == 0:
        return ""
    
    summary = summarize(
        title,
        format_health_bonus(hp),
        f"Melee Damage + {truncate(melee * 100)}%"
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
