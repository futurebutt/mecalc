from collections.abc import Iterable
from enum import Enum, EnumType

from enums import (
    Ability,
    AbsoluteBonus,
    BaseValue,
    Specialization,
    PercentBonus,
    Unlock
)


def validate_enum(en: Enum, entype: EnumType) -> None:
    if en not in entype:
        raise ValueError(f"Not in {entype}: {en}")


class Talent:

    name = "<TALENT>"
    abilities = dict[Enum, dict[int, int]]
    stats = dict[Enum, dict[int, float]]
    traits = dict[Enum, int]

    def __init__(self, rank: int = 0) -> None:
        self.rank = rank

    def _get_ranked_value(self, en: Enum) -> float | int:
        lookup: dict = stats.get(en)
        if lookup is None:
            return 0
        for rank, value in reversed(lookup.items()):
            if self.rank >= rank:
                return value

    def _get_ranked_trait(self, en: Enum) -> bool:
        unlock_rank: int = self.lookups.get(en)
        if unlock_rank is None:
            return False
        return self.rank >= unlock_rank

    def get_ability_rank(self, en: Enum) -> int:
        validate_enum(en, Ability)
        return self._get_ranked_value(en)
    
    def get_absolute_bonus(self, en: Enum) -> float:
        validate_enum(en, AbsoluteBonus)
        return self._get_ranked_value(en)

    def get_base_value(self, en: Enum) -> float:
        validate_enum(en, BaseValue)
        return self._get_ranked_value(en)

    def get_percent_bonus(self, en: Enum) -> float:
        validate_enum(en, PercentBonus)
        return self._get_ranked_value(en)

    def get_specialized(self, en: Enum) -> bool:
        validate_enum(en, Specialization)
        return self._get_ranked_unlock(en)

    def get_unlocked(self, en: Unlock) -> bool:
        validate_enum(en, Unlock)
        return self._get_ranked_unlock(en)


def get_ability_rank(talents: Iterable[Talent], name: Ability) -> int:
    return max(talent.get_ability_rank(name) for talent in talents)


def get_base_value(talents: Iterable[Talent], name: BaseValue) -> float:
    return max(talent.get_base_value(name) for talent in talents)


def get_specialized(talents: Iterable[Talent], name: Specialization) -> bool:
    return any(talent.get_specialized(name) for talent in talents)


def get_total_absolute_bonus(talents: Iterable[Talent], names: Iterable[AbsoluteBonus]) -> float:
    return sum(talent.get_absolute_bonus(name) for name in names for talent in talents)


def get_total_percent_bonus(talents: Iterable[Talent], names: Iterable[PercentBonus]) -> float:
    return sum(talent.get_percent_bonus(name) for name in names for talent in talents)


def get_unlocked(talents: Iterable[Talent], name: Unlock) -> bool:
    return any(talent.get_unlocked(name) for talent in talents)


class Adept(Talent):

    name = "Adept"
    haste = {1: 0.04, 2: 0.06, 3: 0.08, 4: 0.10, 5: 0.12, 6: 0.14}
    bonuses = {
        PercentBonus.BARRIER_HASTE: haste,
        PercentBonus.LIFT_HASTE: haste,
        PercentBonus.SINGULARITY_HASTE: haste,
        PercentBonus.STASIS_HASTE: haste,
        PercentBonus.THROW_HASTE: haste,
        PercentBonus.WARP_HASTE: haste,
        PercentBonus.BIOTIC_PROTECTION: {1: 0.06, 2: 0.09, 3: 0.12, 4: 0.15, 5: 0.18, 6: 0.21},
    }


class AdeptBastion(Adept):

    name = "Bastion"
    haste = {**Adept.haste, 7: 0.18, 8: 0.20, 9: 0.22, 10: 0.24, 11: 0.26, 12: 0.28}
    bonuses = {
        **Adept.bonuses,
        PercentBonus.BARRIER_HASTE: haste,
        PercentBonus.LIFT_HASTE: haste,
        PercentBonus.SINGULARITY_HASTE: haste,
        PercentBonus.STASIS_HASTE: haste,
        PercentBonus.THROW_HASTE: haste,
        PercentBonus.WARP_HASTE: haste,
    }
    unlocks = {
        Specialization.BARRIER: 9,
        Specialization.STASIS: 12,
    }


class AdeptNemesis(Adept):

    name = "Nemesis"
    nemesis_bonus = {7: 0.04, 8: 0.06, 9: 0.08, 10: 0.10, 11: 0.12, 12: 0.14}
    bonuses = {
        **Adept.bonuses,
        PercentBonus.THROW_DAMAGE: nemesis_bonus,
        PercentBonus.THROW_FORCE: nemesis_bonus,
        PercentBonus.BARRIER_DURATION: nemesis_bonus,
        PercentBonus.LIFT_DURATION: nemesis_bonus,
        PercentBonus.SINGULARITY_DURATION: nemesis_bonus,
        PercentBonus.STASIS_DURATION: nemesis_bonus,
        PercentBonus.WARP_DURATION: nemesis_bonus,
    }
    unlocks = {
        Specialization.WARP: 9,
        Specialization.LIFT: 12,
    }


class AssaultRifles(Talent):

    name = "Assault Rifles"
    abilities = {
        Ability.OVERKILL: {1: 1, 8: 2, 12: 3},
    }
    bonuses = {
        PercentBonus.ASSAULT_RIFLE_ACCURACY: {2: 0.10, 3: 0.14, 4: 0.17, 5: 0.20, 6: 0.22, 7: 0.24, 9: 0.26, 10: 0.28, 11: 0.30,},
        PercentBonus.ASSAULT_RIFLE_DAMAGE:   {2: 0.05, 3: 0.08, 4: 0.10, 5: 0.12, 6: 0.14, 7: 0.16, 9: 0.18, 10: 0.19, 11: 0.20,},
    }


class AssaultTraining(Talent):

    name = "Assault Training"
    weapon_damage = {1: 0.01, 2: 0.02, 4: 0.03, 5: 0.04, 6: 0.05, 7: 0.06, 9: 0.07, 10: 0.08, 11: 0.09}
    abilities = {
        Ability.ADRENALINE_BURST: {3: 1, 8: 2, 12: 3},
    }
    bonuses = {
        PercentBonus.MELEE_DAMAGE:  {1: 0.30, 2: 0.35, 4: 0.40, 5: 0.44, 6: 0.48, 7: 0.52, 9: 0.56, 10: 0.60, 11: 0.64},
        PercentBonus.ASSAULT_RIFLE_DAMAGE: weapon_damage,
        PercentBonus.PISTOL_DAMAGE: weapon_damage,
        PercentBonus.SHOTGUN_DAMAGE: weapon_damage,
        PercentBonus.SNIPER_RIFLE_DAMAGE: weapon_damage,
    }


class Barrier(Talent):

    name = "Barrier"
    abilities = {
        Ability.BARRIER: {1: 1, 7: 2, 12: 3},
    }
    base_values = {
        BaseValue.BARRIER_DURATION: {1: 10.0, 2: 10.5, 3: 11.0, 4: 11.5, 5: 12.0, 6: 12.5, 7: 16.5, 8: 17.0, 9: 17.5, 10: 18.0, 11: 18.5, 12: 23.0},
        BaseValue.BARRIER_SHIELDING: {1: 400, 2: 420, 3: 440, 4: 460, 5: 480, 6: 500, 7: 700, 8: 720, 9: 740, 10: 760, 11: 780, 12: 1000},
    }


class BasicArmor(Talent):

    name = "Basic Armor"
    abilities = {
        Ability.SHIELD_BOOST: {3: 1, 8: 2, 12: 3},
    }
    bonuses = {
        PercentBonus.LIGHT_ARMOR_DR:        {1: 0.05, 2: 0.08, 4: 0.10, 5: 0.12, 6: 0.14, 7: 0.16, 9: 0.18, 10: 0.19, 11: 0.20},
        PercentBonus.LIGHT_ARMOR_HARDENING: {1: 0.05, 2: 0.08, 4: 0.10, 5: 0.12, 6: 0.14, 7: 0.16, 9: 0.18, 10: 0.19, 11: 0.20},
    }


class Charm(Talent):

    name = "Charm"
    base_values = {
        BaseValue.CHARM_RANK: {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12}
    }
    bonuses = {}


class CombatArmor(Talent):

    name = "Combat Armor"
    abilities = {
        Ability.SHIELD_BOOST: {3: 1, 8: 2, 12: 3},
    }
    bonuses = {
        PercentBonus.HEAVY_ARMOR_DR:        {1: 0.05, 2: 0.08, 4: 0.10, 5: 0.12, 6: 0.14, 7: 0.16, 9: 0.18, 10: 0.19, 11: 0.20},
        PercentBonus.HEAVY_ARMOR_HARDENING: {1: 0.05, 2: 0.08, 4: 0.10, 5: 0.12, 6: 0.14, 7: 0.16, 9: 0.18, 10: 0.19, 11: 0.20},
    }


class Damping(Talent):

    name = "Damping"
    radius = {2: 0.10, 3: 0.14, 4: 0.18, 5: 0.20, 7: 0.22, 8: 0.24, 9: 0.26, 10: 0.28, 11: 0.30}
    abilities = {
        Ability.DAMPING: {1: 1, 6: 2, 12: 3},
    }
    bonuses = {
        PercentBonus.DAMPING_RADIUS: radius,
        PercentBonus.OVERLOAD_RADIUS: radius,
        PercentBonus.SABOTAGE_RADIUS: radius,
    }


class Decryption(Talent):
    
    name = "Decryption"
    abilities = {
        Ability.SABOTAGE: {1: 1, 5: 2, 9: 3},
    }
    bonuses = {
        PercentBonus.TECH_MINE_DAMAGE: {2: 0.10, 3: 0.14, 4: 0.18, 6: 0.20, 7: 0.22, 8: 0.24, 10: 0.26, 11: 0.28, 12: 0.30},
    }


class Electronics(Talent):

    name = "Electronics"
    abilities = {
        Ability.OVERLOAD: {1: 1, 5: 2, 9: 3},
    }
    bonuses = {
        AbsoluteBonus.HULL_REPAIR: {2: 400, 3: 600, 4: 800, 6: 1200, 7: 1400, 8: 1600, 10: 2000, 11: 2200, 12: 2400},
        AbsoluteBonus.SHIELD_CAPACITY: {2: 30, 3: 60, 4: 90, 6: 120, 7: 150, 8: 180, 10: 210, 11: 240, 12: 270},
    }


class Engineer(Talent):

    name = "Engineer"
    haste = {1: 0.04, 2: 0.06, 3: 0.08, 4: 0.10, 5: 0.12, 6: 0.14}
    bonuses = {
        PercentBonus.AI_HACKING_HASTE: haste,
        PercentBonus.DAMPING_HASTE: haste,
        PercentBonus.FIRST_AID_HASTE: haste,
        PercentBonus.NEURAL_SHOCK_HASTE: haste,
        PercentBonus.OVERLOAD_HASTE: haste,
        PercentBonus.SABOTAGE_HASTE: haste,
        PercentBonus.TECH_PROTECTION: {1: 0.06, 2: 0.09, 3: 0.12, 4: 0.15, 5: 0.18, 6: 0.21},
    }


class EngineerMedic(Engineer):

    name = "Medic"
    tech_haste = {**Engineer.haste, 7: 0.20}
    medic_haste = {7: 0.20, 8: 0.23, 9: 0.26, 10: 0.29, 11: 0.32, 12: 0.35}
    bonuses = {
        **Engineer.bonuses,
        PercentBonus.AI_HACKING_HASTE: tech_haste,
        PercentBonus.DAMPING_HASTE: tech_haste,
        PercentBonus.OVERLOAD_HASTE: tech_haste,
        PercentBonus.SABOTAGE_HASTE: tech_haste,
        PercentBonus.FIRST_AID_HASTE: medic_haste,
        PercentBonus.NEURAL_SHOCK_HASTE: medic_haste,
    }
    unlocks = {
        Specialization.NEURAL_SHOCK: 9,
        Specialization.FIRST_AID: 12,
    }


class EngineerOperative(Engineer):

    name = "Operative"
    haste = {**Engineer.haste, 7: 0.18, 8: 0.20, 9: 0.22, 10: 0.24, 11: 0.26, 12: 0.28}
    bonuses = {
        **Engineer.bonuses,
        PercentBonus.AI_HACKING_HASTE: haste,
        PercentBonus.DAMPING_HASTE: haste,
        PercentBonus.FIRST_AID_HASTE: haste,
        PercentBonus.NEURAL_SHOCK_HASTE: haste,
        PercentBonus.OVERLOAD_HASTE: haste,
        PercentBonus.SABOTAGE_HASTE: haste,
    }
    unlocks = {
        Specialization.OVERLOAD: 9,
        Specialization.SABOTAGE: 12,
    }


class FirstAid(Talent):
    
    name = "First Aid"
    bonuses = {
        AbsoluteBonus.FIRST_AID_HEALING: {1: 40, 2: 50, 3: 60, 4: 70, 5: 80, 6: 100, 7: 110, 8: 120, 9: 130, 10: 140, 11: 150, 12: 180},
    }


class Fitness(Talent):

    name = "Fitness"
    abilities = {
        Ability.IMMUNITY: {4: 1, 8: 2, 12: 3},
    }
    bonuses = {
        PercentBonus.HEALTH: {1: 0.10, 2: 0.14, 3: 0.17, 5: 0.20, 6: 0.22, 7: 0.24, 9: 0.26, 10: 0.28, 11: 0.30},
    }


class Hacking(Talent):

    name = "Hacking"
    haste = {2: 0.06, 3: 0.09, 4: 0.12, 5: 0.15, 6: 0.18, 8: 0.21, 9: 0.24, 10: 0.27, 11: 0.30}
    abilities = {
        Ability.AI_HACKING: {1: 1, 7: 2, 12: 3},
    }
    bonuses = {
        PercentBonus.DAMPING_HASTE: haste,
        PercentBonus.OVERLOAD_HASTE: haste,
        PercentBonus.SABOTAGE_HASTE: haste,
    }


class Infiltrator(Talent):

    name = "Infiltrator"
    bonuses = {
        PercentBonus.PISTOL_COOLING:       {1: 0.05, 2: 0.06, 3: 0.07, 4: 0.08, 5: 0.09, 6: 0.10},
        PercentBonus.SNIPER_RIFLE_COOLING: {1: 0.05, 2: 0.06, 3: 0.07, 4: 0.08, 5: 0.09, 6: 0.10},
        PercentBonus.TECH_MINE_DAMAGE: {1: 0.05, 2: 0.07, 3: 0.09, 4: 0.11, 5: 0.13, 6: 0.15},
    }


class InfiltratorCommando(Infiltrator):

    name = "Commando"
    weapon_damage = {7: 0.06, 8: 0.09, 9: 0.12, 10: 0.15, 11: 0.18, 12: 0.21}
    bonuses = {
        **Infiltrator.bonuses,
        PercentBonus.ASSAULT_RIFLE_DAMAGE: weapon_damage,
        PercentBonus.PISTOL_DAMAGE: weapon_damage,
        PercentBonus.SHOTGUN_DAMAGE: weapon_damage,
        PercentBonus.SNIPER_RIFLE_DAMAGE: weapon_damage,
    }
    unlocks = {
        Specialization.IMMUNITY: 9,
        Specialization.ASSASSINATION: 12,
    }


class InfiltratorOperative(Infiltrator):

    name = "Operative"
    # TODO: It's unclear from language on wiki vs. that used for engineer whether
    # this haste table applies to First Aid and Neural Shock as well as the strictly-
    # "tech" abilities.
    haste = {7: 0.04, 8: 0.06, 9: 0.08, 10: 0.10, 11: 0.12, 12: 0.14}
    bonuses = {
        **Infiltrator.bonuses,
        PercentBonus.AI_HACKING_HASTE: haste,
        PercentBonus.DAMPING_HASTE: haste,
        PercentBonus.FIRST_AID_HASTE: haste,
        PercentBonus.NEURAL_SHOCK_HASTE: haste,
        PercentBonus.OVERLOAD_HASTE: haste,
        PercentBonus.SABOTAGE_HASTE: haste,
    }
    unlocks = {
        Specialization.OVERLOAD: 9,
        Specialization.SABOTAGE: 12,
    }


class Intimidate(Talent):

    name = "Intimidate"
    base_values = {}


class Lift(Talent):

    name = "Lift"
    abilities = {
        Ability.LIFT: {1: 1, 7: 2, 12: 3},
    }
    base_values = {
        BaseValue.LIFT_DURATION: {1: 6.0, 2: 6.4, 3: 6.8, 4: 7.2, 5: 7.6, 6: 8.0, 7: 9.0, 8: 9.4, 9: 9.8, 10: 10.2, 11: 10.6, 12: 12.0},
    }


class Pistols(Talent):

    name = "Pistols"
    abilities = {
        Ability.MARKSMAN: {3: 1, 8: 2, 12: 3},
    }
    bonuses = {
        PercentBonus.PISTOL_ACCURACY: {1: 0.10, 2: 0.14, 4: 0.17, 5: 0.20, 6: 0.22, 7: 0.24, 9: 0.26, 10: 0.28, 11: 0.30,},
        PercentBonus.PISTOL_DAMAGE:   {1: 0.05, 2: 0.08, 4: 0.10, 5: 0.12, 6: 0.14, 7: 0.16, 9: 0.18, 10: 0.19, 11: 0.20,},
    }


class Medicine(Talent):

    name = "Medicine"
    abilities = {
        Ability.NEURAL_SHOCK: {1: 1, 7: 2, 12: 3},
    }
    bonuses = {
        PercentBonus.FIRST_AID_HASTE: {2: 0.10, 3: 0.14, 4: 0.17, 5: 0.20, 6: 0.22, 8: 0.24, 9: 0.26, 10: 0.28, 11: 0.30},
    }


class Sentinel(Talent):

    name = "Sentinel"
    haste = {1: 0.03, 2: 0.05, 3: 0.07, 4: 0.08, 5: 0.09, 6: 0.10}
    ability_table ={
        Ability.MARKSMAN: {6: 1},
    }
    bonuses = {
        PercentBonus.PISTOL_ACCURACY: {1: 0.04, 2: 0.07, 3: 0.10, 4: 0.13, 5: 0.16},
        PercentBonus.PISTOL_DAMAGE: {1: 0.02, 2: 0.04, 3: 0.06, 4: 0.08, 5: 0.10, 6: 0.12},
        PercentBonus.BARRIER_HASTE: haste,
        PercentBonus.LIFT_HASTE: haste,
        PercentBonus.STASIS_HASTE: haste,
        PercentBonus.THROW_HASTE: haste,
        PercentBonus.FIRST_AID_HASTE: haste,
        PercentBonus.NEURAL_SHOCK_HASTE: haste,
        PercentBonus.OVERLOAD_HASTE: haste,
        PercentBonus.SABOTAGE_HASTE: haste,
    }


class SentinelBastion(Sentinel):

    name = "Bastion"
    haste = {**Sentinel.haste, 7: 0.13, 8: 0.15, 9: 0.17, 10: 0.19, 11: 0.21, 12: 0.28}
    bonuses = {
        **Sentinel.bonuses,
        PercentBonus.PISTOL_ACCURACY: {**Sentinel.bonuses[PercentBonus.PISTOL_ACCURACY], 12: 0.23},
        PercentBonus.BARRIER_HASTE: haste,
        PercentBonus.LIFT_HASTE: haste,
        PercentBonus.STASIS_HASTE: haste,
        PercentBonus.THROW_HASTE: haste,
    }
    unlocks = {
        Specialization.BARRIER: 9,
        Specialization.STASIS: 12,
    }


class SentinelMedic(Sentinel):

    name = "Medic"
    haste = {**Sentinel.haste, 7: 0.15}
    medic_haste = {**Sentinel.haste, 7: 0.15, 8: 0.18, 9: 0.21, 10: 0.24, 11: 0.27, 12: 0.30}
    bonuses = {
        **Sentinel.bonuses,
        PercentBonus.BARRIER_HASTE: haste,
        PercentBonus.LIFT_HASTE: haste,
        PercentBonus.STASIS_HASTE: haste,
        PercentBonus.THROW_HASTE: haste,
        PercentBonus.OVERLOAD_HASTE: haste,
        PercentBonus.SABOTAGE_HASTE: haste,
        PercentBonus.FIRST_AID_HASTE: medic_haste,
        PercentBonus.NEURAL_SHOCK_HASTE: medic_haste,
    }
    unlocks = {
        Specialization.NEURAL_SHOCK: 9,
        Specialization.FIRST_AID: 12,
    }


class Shotguns(Talent):

    name = "Shotguns"
    abilities = {
        Ability.CARNAGE: {4: 1, 8: 2, 12: 3},
    }
    bonuses = {
        PercentBonus.SHOTGUN_ACCURACY: {1: 0.10, 2: 0.14, 3: 0.17, 5: 0.20, 6: 0.22, 7: 0.24, 9: 0.26, 10: 0.28, 11: 0.30,},
        PercentBonus.SHOTGUN_DAMAGE:   {1: 0.05, 2: 0.08, 3: 0.10, 5: 0.12, 6: 0.14, 7: 0.16, 9: 0.18, 10: 0.19, 11: 0.20,},
    }


class Singularity(Talent):

    name = "Singularity"
    abilities = {
        Ability.SINGULARITY: {1: 1, 7: 2, 12: 3},
    }
    base_values = {
        BaseValue.SINGULARITY_RADIUS: {1: 4, 2: 4.25, 3: 4.5, 4: 5.0, 6: 5.25, 7: 6.25, 8: 6.5, 9: 6.75, 10: 7.0, 11: 7.25, 12: 8.25},
    }


class Soldier(Talent):

    name = "Soldier"
    bonuses = {
        PercentBonus.HEALTH: {1: 0.04, 2: 0.06, 3: 0.08, 4: 0.10, 5: 0.12, 6: 0.14},
        PercentBonus.HEALTH_REGEN: {1: 3.0, 2: 3.5, 3: 4.0, 4: 4.5, 5: 5.0, 6: 5.5},
    }


class SoldierCommando(Soldier):

    name = "Commando"
    weapon_damage = {7: 0.06, 8: 0.09, 9: 0.12, 10: 0.15, 11: 0.18, 12: 0.21}
    bonuses = {
        **Soldier.bonuses,
        PercentBonus.ASSAULT_RIFLE_DAMAGE: weapon_damage,
        PercentBonus.PISTOL_DAMAGE: weapon_damage,
        PercentBonus.SHOTGUN_DAMAGE: weapon_damage,
        PercentBonus.SNIPER_RIFLE_DAMAGE: weapon_damage,
    }
    unlocks = {
        Specialization.IMMUNITY: 9,
        Specialization.ASSASSINATION: 12,
    }


class SoldierShockTrooper(Soldier):

    name = "Shock Trooper"
    bonuses = {
        **Soldier.bonuses,
        PercentBonus.DAMAGE_PROTECTION: {7: 0.06, 8: 0.08, 9: 0.10, 10: 0.12, 11: 0.14, 12: 0.16},
        PercentBonus.HEALTH: {**Soldier.bonuses[PercentBonus.HEALTH], 7: 0.18, 8: 0.20, 9: 0.22, 10: 0.24, 11: 0.26, 12: 0.28},
    }
    unlocks = {
        Specialization.IMMUNITY: 9,
        Specialization.ADRENALINE_BURST: 12,
    }


class SniperRifles(Talent):

    name = "Sniper Rifles"
    abilities = {
        Ability.ASSASSINATION: {4: 1, 8: 2, 12: 3},
    }
    bonuses = {
        PercentBonus.SNIPER_RIFLE_ACCURACY: {1: 0.10, 2: 0.14, 4: 0.17, 5: 0.20, 6: 0.22, 7: 0.24, 9: 0.26, 10: 0.28, 11: 0.30,},
        PercentBonus.SNIPER_RIFLE_DAMAGE:   {1: 0.05, 2: 0.08, 4: 0.10, 5: 0.12, 6: 0.14, 7: 0.16, 9: 0.18, 10: 0.19, 11: 0.20,},
    }


class SpectreTraining(Talent):

    name = "Spectre Training"
    abilities = {
        Ability.UNITY: {4: 1, 8: 2, 12: 3},
    }
    bonuses = {
        PercentBonus.ACCURACY_REGEN: {1: 0.004, 2: 0.006, 3: 0.008, 5: 0.01, 6: 0.012, 7: 0.014, 9: 0.016, 10: 0.018, 11: 0.02},
        PercentBonus.ALL_DAMAGE:   {1: 0.01, 2: 0.015, 3: 0.02, 5: 0.025, 6: 0.03, 7: 0.035, 9: 0.04, 10: 0.045, 11: 0.05},
        PercentBonus.ALL_DURATIONS: {1: 0.01, 2: 0.015, 3: 0.02, 5: 0.025, 6: 0.03, 7: 0.035, 9: 0.04, 10: 0.045, 11: 0.05},
        PercentBonus.HEALTH: {1: 0.05, 2: 0.055, 3: 0.06, 5: 0.065, 6: 0.07, 7: 0.075, 9: 0.08, 10: 0.085, 11: 0.09},
        PercentBonus.MAX_ACCURACY: {1: 0.02, 2: 0.03, 3: 0.04, 5: 0.05, 6: 0.06, 7: 0.07, 9: 0.08, 10: 0.09, 11: 0.10},
    }


class Stasis(Talent):

    name = "Stasis"
    abilities = {
        Ability.STASIS: {1: 1, 6: 2, 12: 3},
    }
    base_values = {
        BaseValue.STASIS_DURATION: {1: 12.5, 2: 13, 3: 13.5, 4: 14, 5: 14.5, 6: 17, 7: 17.5, 8: 18, 9: 18.5, 10: 19, 11: 19.5, 12: 21},
    }


class TacticalArmor(Talent):

    name = "Tactical Armor"
    abilities = {
        Ability.SHIELD_BOOST: {3: 1, 8: 2, 12: 3},
    }
    bonuses = {
        PercentBonus.MED_ARMOR_DR:        {1: 0.05, 2: 0.08, 4: 0.10, 5: 0.12, 6: 0.14, 7: 0.16, 9: 0.18, 10: 0.19, 11: 0.20},
        PercentBonus.MED_ARMOR_HARDENING: {1: 0.05, 2: 0.08, 4: 0.10, 5: 0.12, 6: 0.14, 7: 0.16, 9: 0.18, 10: 0.19, 11: 0.20},
    }


class Throw(Talent):

    name = "Throw"
    abilities = {
        Ability.THROW: {1: 1, 8: 2, 12: 3},
    }
    base_values = {
        BaseValue.THROW_FORCE: {1: 600, 2: 650, 3: 700, 4: 750, 5: 800, 6: 850, 7: 900, 8: 1000, 9: 1050, 10: 1100, 11: 1150, 12: 1250},
    }


class Vanguard(Talent):

    name = "Vanguard"
    bonuses = {
        PercentBonus.BIOTIC_PROTECTION: {1: 0.06, 2: 0.09, 3: 0.12, 4: 0.15, 5: 0.18, 6: 0.21},
        PercentBonus.PISTOL_DAMAGE:  {1: 0.05, 2: 0.06, 3: 0.07, 4: 0.08, 5: 0.09, 6: 0.10},
        PercentBonus.SHOTGUN_DAMAGE: {1: 0.05, 2: 0.06, 3: 0.07, 4: 0.08, 5: 0.09, 6: 0.10},
    }


class VanguardNemesis(Vanguard):

    name = "Nemesis"
    nemesis_bonus = {7: 0.04, 8: 0.06, 9: 0.08, 10: 0.10, 11: 0.12, 12: 0.14}
    bonuses = {
        **Vanguard.bonuses,
        PercentBonus.THROW_DAMAGE: nemesis_bonus,
        PercentBonus.THROW_FORCE: nemesis_bonus,
        PercentBonus.BARRIER_DURATION: nemesis_bonus,
        PercentBonus.LIFT_DURATION: nemesis_bonus,
        PercentBonus.WARP_DURATION: nemesis_bonus,        
    }
    unlocks = {
        Specialization.WARP: 9,
        Specialization.LIFT: 12,
    }


class VanguardShockTrooper(Vanguard):

    name = "Shock Trooper"
    bonuses = {
        **Vanguard.bonuses,
        PercentBonus.HEALTH: {7: 0.04, 8: 0.06, 9: 0.08, 10: 0.10, 11: 0.12, 12: 0.14},
        PercentBonus.DAMAGE_PROTECTION: {7: 0.06, 8: 0.08, 9: 0.10, 10: 0.12, 11: 0.14, 12: 0.16},
    }
    unlocks = {
        Specialization.BARRIER: 9,
        Specialization.ADRENALINE_BURST: 12,
    }


class Warp(Talent):

    name = "Warp"
    abilities = {
        Ability.WARP: {1: 1, 6: 2, 12: 3},
    }
    base_values = {
        BaseValue.WARP_DURATION: {1: 7, 2: 8, 3: 9, 4: 10, 5: 11, 6: 13, 7: 14, 8: 15, 9: 16, 10: 17, 11: 18, 12: 20},
    }
