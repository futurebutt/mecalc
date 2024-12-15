from collections.abc import Iterable
from enum import auto, Enum


class PercentModifier(Enum):
    HEALTH = auto()
    MELEE_DAMAGE = auto()
    PISTOL_ACCURACY = auto()
    PISTOL_DAMAGE = auto()
    WEAPON_DAMAGE = auto()


class AbilityRank(Enum):
    MARKSMAN = auto()


# Rank -> Bonus at Rank
Levels = dict[int, float]


class Talent:

    name: str = "<TALENT>"
    levelup_table: dict[PercentModifier, Levels] = {}

    def __init__(self, rank: int):
        self.rank: int = rank
        self.bonuses: dict[PercentModifier, float] = {}
        self.abilities: dict[AbilityRank, float] = {}

    def calculate_bonuses(self):
        for feature, ranks in self.levelup_table.items():
            best_value = 0
            for threshold, value in ranks.items():
                if self.rank >= threshold:
                    best_value = value

            if isinstance(feature, PercentModifier):
                self.bonuses[feature] = best_value

            elif isinstance(feature, AbilityRank):
                self.abilities[feature] = best_value

    def get_bonuses(self) -> dict[PercentModifier, float]:
        self.calculate_bonuses()
        return self.bonuses

    def get_abilities(self) -> dict[AbilityRank, int]:
        self.calculate_bonuses()
        return self.abilities


class TalentAssaultTraining(Talent):

    name = "Assault Training"
    levelup_table = {
        PercentModifier.MELEE_DAMAGE:  {1: 0.30, 2: 0.35, 4: 0.40, 5: 0.44, 6: 0.48, 7: 0.52, 9: 0.56, 10: 0.60, 11: 0.64},
        PercentModifier.WEAPON_DAMAGE: {1: 0.01, 2: 0.02, 4: 0.03, 5: 0.04, 6: 0.05, 7: 0.06, 9: 0.07, 10: 0.08, 11: 0.09},
    }


class TalentFitness(Talent):

    name = "Fitness"
    levelup_table = {
        PercentModifier.HEALTH: {1: 0.10, 2: 0.14, 3: 0.17, 5: 0.20, 6: 0.22, 7: 0.24, 9: 0.26, 10: 0.28, 11: 0.30},
    }


class TalentPistols(Talent):

    name = "Pistols"
    levelup_table = {
        PercentModifier.PISTOL_ACCURACY: {1: 0.10, 2: 0.14, 4: 0.17, 5: 0.20, 6: 0.22, 7: 0.24, 9: 0.26, 10: 0.28, 11: 0.30,},
        PercentModifier.PISTOL_DAMAGE:   {1: 0.05, 2: 0.08, 4: 0.10, 5: 0.12, 6: 0.14, 7: 0.16, 9: 0.18, 10: 0.19, 11: 0.20,},
        AbilityRank.MARKSMAN: {3: 1, 8: 2, 12: 3},
    }


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
