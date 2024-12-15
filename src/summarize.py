from collections.abc import Iterable

from enums import AbilityLevel, PercentModifier
from talents import Talent


def calculate_bonus(talents: Iterable[Talent], dependencies: Iterable[PercentModifier]) -> float:
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


def percent(value: float) -> float:
    return round(100 * value, 3)


def format_modifier(label: str, value: float) -> str:
    return f"    {label} + {percent(value)}%"


def format_flat_percent(label: str, value: float) -> str:
    return f"    {label} {percent(value)}%"


def format_duration(label: str, value: float) -> str:
    return f"    {label} {value} sec"


def format_distance(label: str, value: float) -> str:
    return f"    {label} {value} m"


def summarize_object(
        title:          str,
        modifiers:      dict[str, float] = {},
        durations:      dict[str, float] = {},
        flat_percents:  dict[str, float] = {},
        distances:      dict[str, float] = {},
        order:          Iterable[str] = ["modifiers", "durations", "flat_percents", "distances"],
    ) -> str:
    summary_lines: list[str] = [title]
    for category in order:
        if category == "modifiers":
            summary_lines.extend(format_modifier(label, value) for label, value in modifiers.items() if value != 0)
        elif category == "durations":
            summary_lines.extend(format_duration(label, value) for label, value in durations.items())
        elif category == "flat_percents":
            summary_lines.extend(format_flat_percent(label, value) for label, value in flat_percents.items())
        elif category == "distances":
            summary_lines.extend(format_distance(label, value) for label, value in distances.items())
    summary = "\n".join(summary_lines)
    return summary


def summarize_Adrenaline_Burst(talents: Iterable[Talent]) -> str:
    rank = get_ability_level(talents, AbilityLevel.ADRENALINE_BURST)
    if rank == 0:
        return ""

    title = "Adrenaline Burst" + {1: "", 2: " (Advanced)", 3: " (Master)"}[rank]
    recharge = {1: 120, 2: 90, 3: 45}[rank]
    accuracy_cost = 0.30

    durations = {"Recharge": recharge}
    flat_percents = {"Accuracy Cost": accuracy_cost}
    summary = summarize_object(title, durations=durations, flat_percents=flat_percents)
    return summary


def summarize_Assault_Rifle(talents: Iterable[Talent]) -> str:
    damage = calculate_bonus(talents, (PercentModifier.ASSAULT_RIFLE_DAMAGE, PercentModifier.WEAPON_DAMAGE))
    accuracy = calculate_bonus(talents, (PercentModifier.ASSAULT_RIFLE_ACCURACY, ))
    if damage == accuracy == 0:
        return ""

    modifiers = {"Damage": damage, "Accuracy": accuracy}
    summary = summarize_object("Assault Rifle", modifiers=modifiers)
    return summary


def summarize_Carnage(talents: Iterable[Talent]) -> str:
    rank = get_ability_level(talents, AbilityLevel.CARNAGE)
    if rank == 0:
        return ""

    title = "Carnage" + {1: "", 2: " (Advanced)", 3: " (Master)"}[rank]
    damage_dps = {1: 2.00, 2: 2.25, 3: 2.50}[rank]
    radius = {1: 2, 2: 2.5, 3: 3}[rank]
    duration = 6
    recharge = 45

    flat_percents = {"Damage": damage_dps}
    distances = {"Radius": radius}
    durations = {"Duration": duration, "Recharge": recharge}
    summary = summarize_object(title, flat_percents=flat_percents, distances=distances, durations=durations, order=["flat_percents", "distances", "durations"])
    return summary


def summarize_Immunity(talents: Iterable[Talent]) -> str:
    rank = get_ability_level(talents, AbilityLevel.IMMUNITY)
    if rank == 0:
        return ""

    title = "Immunity" + {1: "", 2: " (Advanced)", 3: " (Master)"}[rank]
    damage_reduction = {1: 0.75, 2: 0.85, 3: 0.90}[rank]
    duration = 6
    recharge = 45

    flat_percents = {"Damage Reduction": damage_reduction}
    durations = {"Duration": duration, "Recharge": recharge}
    summary = summarize_object(title, durations=durations, flat_percents=flat_percents, order=["flat_percents", "durations"])
    return summary


def summarize_Marksman(talents: Iterable[Talent]) -> str:
    rank = get_ability_level(talents, AbilityLevel.MARKSMAN)
    if rank == 0:
        return ""

    title = "Marksman" + {1: "", 2: " (Advanced)", 3: " (Master)"}[rank]
    accuracy = 0.60
    damage = {1: 0.25, 2: 0.50, 3: 0.75}[rank]
    headshot_damage = {1: 0.50, 2: 0.75, 3: 1.00}[rank]
    duration = 6
    recharge = 45

    modifiers = {"Accuracy": accuracy, "Damage": damage, "Headshot Damage": headshot_damage}
    durations = {"Duration": duration, "Recharge": recharge}
    summary = summarize_object(title, modifiers=modifiers, durations=durations)
    return summary


def summarize_Overkill(talents: Iterable[Talent]) -> str:
    rank = get_ability_level(talents, AbilityLevel.OVERKILL)
    if rank == 0:
        return ""

    title = "Overkill" + {1: "", 2: " (Advanced)", 3: " (Master)"}[rank]
    heat_reduction = {1: 0.80, 2: 0.90, 3: 1.00}[rank]
    damage = {1: 0.50, 2: 0.75, 3: 1.00}[rank]
    duration = 6
    recharge = 45

    flat_percents = {"Heat Reduction": heat_reduction}
    modifiers = {"Damage": damage, "Headshot Damage": damage}
    durations = {"Duration": duration, "Recharge": recharge}
    summary = summarize_object(title, flat_percents=flat_percents, modifiers=modifiers, durations=durations, order=["flat_percents", "modifiers", "durations"])
    return summary


def summarize_Pistol(talents: Iterable[Talent]) -> str:
    damage = calculate_bonus(talents, (PercentModifier.PISTOL_DAMAGE, PercentModifier.WEAPON_DAMAGE))
    accuracy = calculate_bonus(talents, (PercentModifier.PISTOL_ACCURACY, ))
    if damage == accuracy == 0:
        return ""

    modifiers = {"Damage": damage, "Accuracy": accuracy}
    summary = summarize_object("Pistol", modifiers=modifiers)
    return summary


def summarize_Shepard(talents: Iterable[Talent]) -> str:
    hp = calculate_bonus(talents, (PercentModifier.HEALTH, ))
    melee = calculate_bonus(talents, (PercentModifier.MELEE_DAMAGE, ))
    if hp == melee == 0:
        return ""
    modifiers = {"Health": hp, "Melee Damage": melee}
    summary = summarize_object("Shepard", modifiers=modifiers)
    return summary


def summarize_Shotgun(talents: Iterable[Talent]) -> str:
    damage = calculate_bonus(talents, (PercentModifier.SHOTGUN_DAMAGE, PercentModifier.WEAPON_DAMAGE))
    accuracy = calculate_bonus(talents, (PercentModifier.SHOTGUN_ACCURACY, ))
    if damage == accuracy == 0:
        return ""

    modifiers = {"Damage": damage, "Accuracy": accuracy}
    summary = summarize_object("Shotgun", modifiers=modifiers)
    return summary


def summarize_Sniper_Rifles(talents: Iterable[Talent]) -> str:
    damage = calculate_bonus(talents, (PercentModifier.SNIPER_RIFLE_DAMAGE, PercentModifier.WEAPON_DAMAGE))
    accuracy = calculate_bonus(talents, (PercentModifier.SNIPER_RIFLE_ACCURACY, ))
    if damage == accuracy == 0:
        return ""

    modifiers = {"Damage": damage, "Accuracy": accuracy}
    summary = summarize_object("Sniper Rifle", modifiers=modifiers)
    return summary


def summarize_Assassination(talents: Iterable[Talent]) -> str:
    rank = get_ability_level(talents, AbilityLevel.ASSASSINATION)
    if rank == 0:
        return ""

    title = "Assassination" + {1: "", 2: " (Advanced)", 3: " (Master)"}[rank]
    damage_dps = {1: 2.00, 2: 2.50, 3: 3.00}[rank]
    duration = 6
    recharge = 45

    flat_percents = {"Damage": damage_dps}
    durations = {"Duration": duration, "Recharge": recharge}
    summary = summarize_object(title, flat_percents=flat_percents, durations=durations, order=["flat_percents", "durations"])
    return summary
