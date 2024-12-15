from collections.abc import Iterable

from enums import AbilityRank, PercentModifier
from talents import Talent


def calculate_bonus(talents: Iterable[Talent], dependencies: Iterable[PercentModifier]) -> float:
    value: float = 0.0
    for talent in talents:
        bonuses = talent.get_bonuses()
        for dep in dependencies:
            value += bonuses.get(dep, 0)
    return value


def get_ability_rank(talents: Iterable[Talent], dependency: AbilityRank) -> int:
    rank: int = 0
    for talent in talents:
        abilities = talent.get_abilities()
        rank = max(rank, abilities.get(dependency, 0))
    return rank


def percent(value: float) -> float:
    return round(100 * value, 3)


def format_percent(label: str, value: float) -> str:
    return f"    {label} + {percent(value)} %"


def format_duration(label: str, value: float) -> str:
    return f"    {label} {value} sec"


def summarize_object(title: str, modifiers: dict[str, float] = {}, durations: dict[str, float] = {}) -> str:
    summary_lines: list[str] = [title]
    summary_lines.extend(format_percent(label, value) for label, value in modifiers.items() if value != 0)
    summary_lines.extend(format_duration(label, value) for label, value in durations.items())
    summary = "\n".join(summary_lines)
    return summary


def summarize_Shepard(talents: Iterable[Talent]) -> str:
    hp = calculate_bonus(talents, (PercentModifier.HEALTH, ))
    melee = calculate_bonus(talents, (PercentModifier.MELEE_DAMAGE, ))
    if hp == melee == 0:
        return ""
    modifiers = {"Health": hp, "Melee Damage": melee}
    summary = summarize_object("Shepard", modifiers=modifiers)
    return summary


def summarize_Pistol(talents: Iterable[Talent]) -> str:
    dmg = calculate_bonus(talents, (PercentModifier.PISTOL_DAMAGE, PercentModifier.WEAPON_DAMAGE))
    acc = calculate_bonus(talents, (PercentModifier.PISTOL_ACCURACY, ))
    if dmg == acc == 0:
        return ""

    modifiers = {"Damage": dmg, "Accuracy": acc}
    summary = summarize_object("Pistol", modifiers=modifiers)
    return summary


def summarize_Marksman(talents: Iterable[Talent]) -> str:
    rank = get_ability_rank(talents, AbilityRank.MARKSMAN)
    if rank == 0:
        return ""

    dmg = {1: 0.25, 2: 0.50, 3: 0.75}[rank]
    headshot = {1: 0.50, 2: 0.75, 3: 1.00}[rank]
    title = "Marksman" + {1: "", 2: " (Advanced)", 3: " (Master)"}[rank]

    modifiers = {"Accuracy": 0.60, "Damage": dmg, "Headshot Damage": headshot}
    durations = {"Duration": 6, "Recharge": 45}
    summary = summarize_object(title, modifiers=modifiers, durations=durations)
    return summary
