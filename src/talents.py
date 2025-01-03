from enums import AbilityLevel, BaseValue, Specialization, Modifier

# Rank -> Value at Rank
Lookup = dict[int, float]


class Talent:

    name: str = "<TALENT>"
    ability_table: dict[AbilityLevel, Lookup] = {}
    modifier_table: dict[Modifier, Lookup] = {}

    def __init__(self, rank: int):
        self.rank: int = rank
        self.modifiers: dict[Modifier, float] = {}
        self.ability_levels: dict[AbilityLevel, float] = {}

    def calculate_modifiers(self):
        for modifier, values in self.modifier_table.items():
            best_value = 0
            for threshold, value in values.items():
                if self.rank >= threshold:
                    best_value = value
            self.modifiers[modifier] = best_value

    def calculate_ability_levels(self):
        # TODO: Happens to cover ability specialization unlocks, but this should
        # be made more explicit.
        for ability, level_lookup in self.ability_table.items():
            best_level: int = 0
            for threshold, level in level_lookup.items():
                if self.rank >= threshold:
                    best_level = level
            self.ability_levels[ability] = best_level

    def get_modifiers(self) -> dict[Modifier, float]:
        self.calculate_modifiers()
        return self.modifiers

    def get_abilities(self) -> dict[AbilityLevel, int]:
        self.calculate_ability_levels()
        return self.ability_levels
    

class Adept(Talent):

    name = "Adept"
    haste = {1: 0.04, 2: 0.06, 3: 0.08, 4: 0.10, 5: 0.12, 6: 0.14}
    modifier_table = {
        Modifier.BARRIER_HASTE: haste,
        Modifier.LIFT_HASTE: haste,
        Modifier.SINGULARITY_HASTE: haste,
        Modifier.STASIS_HASTE: haste,
        Modifier.THROW_HASTE: haste,
        Modifier.WARP_HASTE: haste,
        Modifier.BIOTIC_PROTECTION: {1: 0.06, 2: 0.09, 3: 0.12, 4: 0.15, 5: 0.18, 6: 0.21},
    }


class AdeptBastion(Adept):

    name = "Bastion"
    haste = {**Adept.haste, 7: 0.18, 8: 0.20, 9: 0.22, 10: 0.24, 11: 0.26, 12: 0.28}
    ability_table = {
        Specialization.BARRIER: {9: True},
        Specialization.STASIS: {12: True},
    }
    modifier_table = {
        **Adept.modifier_table,
        Modifier.BARRIER_HASTE: haste,
        Modifier.LIFT_HASTE: haste,
        Modifier.SINGULARITY_HASTE: haste,
        Modifier.STASIS_HASTE: haste,
        Modifier.THROW_HASTE: haste,
        Modifier.WARP_HASTE: haste,
    }


class AdeptNemesis(Adept):

    name = "Nemesis"
    nemesis_bonus = {7: 0.04, 8: 0.06, 9: 0.08, 10: 0.10, 11: 0.12, 12: 0.14}
    ability_table = {
        Specialization.WARP: {9: True},
        Specialization.LIFT: {12: True},
    }
    modifier_table = {
        **Adept.modifier_table,
        Modifier.THROW_DAMAGE: nemesis_bonus,
        Modifier.THROW_FORCE: nemesis_bonus,
        Modifier.BARRIER_DURATION: nemesis_bonus,
        Modifier.LIFT_DURATION: nemesis_bonus,
        Modifier.SINGULARITY_DURATION: nemesis_bonus,
        Modifier.STASIS_DURATION: nemesis_bonus,
        Modifier.WARP_DURATION: nemesis_bonus,
    }


class AssaultRifles(Talent):

    name = "Assault Rifles"
    ability_table = {
        AbilityLevel.OVERKILL: {1: 1, 8: 2, 12: 3},
    }
    modifier_table = {
        Modifier.ASSAULT_RIFLE_ACCURACY: {2: 0.10, 3: 0.14, 4: 0.17, 5: 0.20, 6: 0.22, 7: 0.24, 9: 0.26, 10: 0.28, 11: 0.30,},
        Modifier.ASSAULT_RIFLE_DAMAGE:   {2: 0.05, 3: 0.08, 4: 0.10, 5: 0.12, 6: 0.14, 7: 0.16, 9: 0.18, 10: 0.19, 11: 0.20,},
    }


class AssaultTraining(Talent):

    name = "Assault Training"
    weapon_damage = {1: 0.01, 2: 0.02, 4: 0.03, 5: 0.04, 6: 0.05, 7: 0.06, 9: 0.07, 10: 0.08, 11: 0.09}
    ability_table = {
        AbilityLevel.ADRENALINE_BURST: {3: 1, 8: 2, 12: 3},
    }
    modifier_table = {
        Modifier.MELEE_DAMAGE:  {1: 0.30, 2: 0.35, 4: 0.40, 5: 0.44, 6: 0.48, 7: 0.52, 9: 0.56, 10: 0.60, 11: 0.64},
        Modifier.ASSAULT_RIFLE_DAMAGE: weapon_damage,
        Modifier.PISTOL_DAMAGE: weapon_damage,
        Modifier.SHOTGUN_DAMAGE: weapon_damage,
        Modifier.SNIPER_RIFLE_DAMAGE: weapon_damage,
    }


class Barrier(Talent):

    name = "Barrier"
    ability_table = {
        AbilityLevel.BARRIER: {1: 1, 7: 2, 12: 3},
    }
    modifier_table = {
        BaseValue.BARRIER_DURATION: {1: 10.0, 2: 10.5, 3: 11.0, 4: 11.5, 5: 12.0, 6: 12.5, 7: 16.5, 8: 17.0, 9: 17.5, 10: 18.0, 11: 18.5, 12: 23.0},
        BaseValue.BARRIER_SHIELDING: {1: 400, 2: 420, 3: 440, 4: 460, 5: 480, 6: 500, 7: 700, 8: 720, 9: 740, 10: 760, 11: 780, 12: 1000},
    }


class BasicArmor(Talent):

    name = "Basic Armor"
    ability_table = {
        AbilityLevel.SHIELD_BOOST: {3: 1, 8: 2, 12: 3},
    }
    modifier_table = {
        Modifier.LIGHT_ARMOR_DR:        {1: 0.05, 2: 0.08, 4: 0.10, 5: 0.12, 6: 0.14, 7: 0.16, 9: 0.18, 10: 0.19, 11: 0.20},
        Modifier.LIGHT_ARMOR_HARDENING: {1: 0.05, 2: 0.08, 4: 0.10, 5: 0.12, 6: 0.14, 7: 0.16, 9: 0.18, 10: 0.19, 11: 0.20},
    }


class Charm(Talent):

    name = "Charm"
    modifier_table = {}


class CombatArmor(Talent):

    name = "Combat Armor"
    ability_table = {
        AbilityLevel.SHIELD_BOOST: {3: 1, 8: 2, 12: 3},
    }
    modifier_table = {
        Modifier.HEAVY_ARMOR_DR:        {1: 0.05, 2: 0.08, 4: 0.10, 5: 0.12, 6: 0.14, 7: 0.16, 9: 0.18, 10: 0.19, 11: 0.20},
        Modifier.HEAVY_ARMOR_HARDENING: {1: 0.05, 2: 0.08, 4: 0.10, 5: 0.12, 6: 0.14, 7: 0.16, 9: 0.18, 10: 0.19, 11: 0.20},
    }


class Damping(Talent):

    name = "Damping"
    radius = {2: 0.10, 3: 0.14, 4: 0.18, 5: 0.20, 7: 0.22, 8: 0.24, 9: 0.26, 10: 0.28, 11: 0.30}
    ability_table = {
        AbilityLevel.DAMPING: {1: 1, 6: 2, 12: 3},
    }
    modifier_table = {
        Modifier.DAMPING_RADIUS: radius,
        Modifier.OVERLOAD_RADIUS: radius,
        Modifier.SABOTAGE_RADIUS: radius,
    }


class Decryption(Talent):
    
    name = "Decryption"
    ability_table = {
        AbilityLevel.SABOTAGE: {1: 1, 5: 2, 9: 3},
    }
    modifier_table = {
        Modifier.TECH_MINE_DAMAGE: {2: 0.10, 3: 0.14, 4: 0.18, 6: 0.20, 7: 0.22, 8: 0.24, 10: 0.26, 11: 0.28, 12: 0.30},
    }


class Electronics(Talent):

    name = "Electronics"
    ability_table = {
        AbilityLevel.OVERLOAD: {1: 1, 5: 2, 9: 3},
    }
    modifier_table = {
        Modifier.HULL_REPAIR: {2: 400, 3: 600, 4: 800, 6: 1200, 7: 1400, 8: 1600, 10: 2000, 11: 2200, 12: 2400},
        Modifier.SHIELD_CAPACITY: {2: 30, 3: 60, 4: 90, 6: 120, 7: 150, 8: 180, 10: 210, 11: 240, 12: 270},
    }


class Engineer(Talent):

    name = "Engineer"
    haste = {1: 0.04, 2: 0.06, 3: 0.08, 4: 0.10, 5: 0.12, 6: 0.14}
    modifier_table = {
        Modifier.AI_HACKING_HASTE: haste,
        Modifier.DAMPING_HASTE: haste,
        Modifier.FIRST_AID_HASTE: haste,
        Modifier.NEURAL_SHOCK_HASTE: haste,
        Modifier.OVERLOAD_HASTE: haste,
        Modifier.SABOTAGE_HASTE: haste,
        Modifier.TECH_PROTECTION: {1: 0.06, 2: 0.09, 3: 0.12, 4: 0.15, 5: 0.18, 6: 0.21},
    }


class EngineerMedic(Engineer):

    name = "Medic"
    tech_haste = {**Engineer.haste, 7: 0.20}
    medic_haste = {7: 0.20, 8: 0.23, 9: 0.26, 10: 0.29, 11: 0.32, 12: 0.35}
    ability_table = {
        Specialization.NEURAL_SHOCK: {9: True},
        Specialization.FIRST_AID: {12: True},
    }
    modifier_table = {
        **Engineer.modifier_table,
        Modifier.AI_HACKING_HASTE: tech_haste,
        Modifier.DAMPING_HASTE: tech_haste,
        Modifier.OVERLOAD_HASTE: tech_haste,
        Modifier.SABOTAGE_HASTE: tech_haste,
        Modifier.FIRST_AID_HASTE: medic_haste,
        Modifier.NEURAL_SHOCK_HASTE: medic_haste,
    }


class EngineerOperative(Engineer):

    name = "Operative"
    haste = {**Engineer.haste, 7: 0.18, 8: 0.20, 9: 0.22, 10: 0.24, 11: 0.26, 12: 0.28}
    ability_table = {
        Specialization.OVERLOAD: {9: True},
        Specialization.SABOTAGE: {12: True},
    }
    modifier_table = {
        **Engineer.modifier_table,
        Modifier.AI_HACKING_HASTE: haste,
        Modifier.DAMPING_HASTE: haste,
        Modifier.FIRST_AID_HASTE: haste,
        Modifier.NEURAL_SHOCK_HASTE: haste,
        Modifier.OVERLOAD_HASTE: haste,
        Modifier.SABOTAGE_HASTE: haste,
    }


class FirstAid(Talent):
    
    name = "First Aid"
    modifier_table = {
        Modifier.FIRST_AID_HEALING: {1: 40, 2: 50, 3: 60, 4: 70, 5: 80, 6: 100, 7: 110, 8: 120, 9: 130, 10: 140, 11: 150, 12: 180},
    }


class Fitness(Talent):

    name = "Fitness"
    ability_table = {
        AbilityLevel.IMMUNITY: {4: 1, 8: 2, 12: 3},
    }
    modifier_table = {
        Modifier.HEALTH: {1: 0.10, 2: 0.14, 3: 0.17, 5: 0.20, 6: 0.22, 7: 0.24, 9: 0.26, 10: 0.28, 11: 0.30},
    }


class Hacking(Talent):

    name = "Hacking"
    haste = {2: 0.06, 3: 0.09, 4: 0.12, 5: 0.15, 6: 0.18, 8: 0.21, 9: 0.24, 10: 0.27, 11: 0.30}
    ability_table = {
        AbilityLevel.AI_HACKING: {1: 1, 7: 2, 12: 3},
    }
    modifier_table = {
        Modifier.DAMPING_HASTE: haste,
        Modifier.OVERLOAD_HASTE: haste,
        Modifier.SABOTAGE_HASTE: haste,
    }


class Infiltrator(Talent):

    name = "Infiltrator"
    modifier_table = {
        Modifier.PISTOL_COOLING:       {1: 0.05, 2: 0.06, 3: 0.07, 4: 0.08, 5: 0.09, 6: 0.10},
        Modifier.SNIPER_RIFLE_COOLING: {1: 0.05, 2: 0.06, 3: 0.07, 4: 0.08, 5: 0.09, 6: 0.10},
        Modifier.TECH_MINE_DAMAGE: {1: 0.05, 2: 0.07, 3: 0.09, 4: 0.11, 5: 0.13, 6: 0.15},
    }


class InfiltratorCommando(Infiltrator):

    name = "Commando"
    weapon_damage = {7: 0.06, 8: 0.09, 9: 0.12, 10: 0.15, 11: 0.18, 12: 0.21}
    ability_table = {
        Specialization.IMMUNITY: {9: True},
        Specialization.ASSASSINATION: {12: True},
    }
    modifier_table = {
        **Infiltrator.modifier_table,
        Modifier.ASSAULT_RIFLE_DAMAGE: weapon_damage,
        Modifier.PISTOL_DAMAGE: weapon_damage,
        Modifier.SHOTGUN_DAMAGE: weapon_damage,
        Modifier.SNIPER_RIFLE_DAMAGE: weapon_damage,
    }


class InfiltratorOperative(Infiltrator):

    name = "Operative"
    # TODO: It's unclear from language on wiki vs. that used for engineer whether
    # this haste table applies to First Aid and Neural Shock as well as the strictly-
    # "tech" abilities.
    haste = {7: 0.04, 8: 0.06, 9: 0.08, 10: 0.10, 11: 0.12, 12: 0.14}
    ability_table = {
        Specialization.OVERLOAD: {9: True},
        Specialization.SABOTAGE: {12: True},
    }
    modifier_table = {
        **Infiltrator.modifier_table,
        Modifier.AI_HACKING_HASTE: haste,
        Modifier.DAMPING_HASTE: haste,
        Modifier.FIRST_AID_HASTE: haste,
        Modifier.NEURAL_SHOCK_HASTE: haste,
        Modifier.OVERLOAD_HASTE: haste,
        Modifier.SABOTAGE_HASTE: haste,
    }


class Intimidate(Talent):

    name = "Intimidate"
    modifier_table = {}


class Lift(Talent):

    name = "Lift"
    ability_table = {
        AbilityLevel.LIFT: {1: 1, 7: 2, 12: 3},
    }
    modifier_table = {
        BaseValue.LIFT_DURATION: {1: 6.0, 2: 6.4, 3: 6.8, 4: 7.2, 5: 7.6, 6: 8.0, 7: 9.0, 8: 9.4, 9: 9.8, 10: 10.2, 11: 10.6, 12: 12.0},
    }


class Pistols(Talent):

    name = "Pistols"
    ability_table = {
        AbilityLevel.MARKSMAN: {3: 1, 8: 2, 12: 3},
    }
    modifier_table = {
        Modifier.PISTOL_ACCURACY: {1: 0.10, 2: 0.14, 4: 0.17, 5: 0.20, 6: 0.22, 7: 0.24, 9: 0.26, 10: 0.28, 11: 0.30,},
        Modifier.PISTOL_DAMAGE:   {1: 0.05, 2: 0.08, 4: 0.10, 5: 0.12, 6: 0.14, 7: 0.16, 9: 0.18, 10: 0.19, 11: 0.20,},
    }


class Medicine(Talent):

    name = "Medicine"
    ability_table = {
        AbilityLevel.NEURAL_SHOCK: {1: 1, 7: 2, 12: 3},
    }
    modifier_table = {
        Modifier.FIRST_AID_HASTE: {2: 0.10, 3: 0.14, 4: 0.17, 5: 0.20, 6: 0.22, 8: 0.24, 9: 0.26, 10: 0.28, 11: 0.30},
    }


class Sentinel(Talent):

    name = "Sentinel"
    haste = {1: 0.03, 2: 0.05, 3: 0.07, 4: 0.08, 5: 0.09, 6: 0.10}
    ability_table ={
        AbilityLevel.MARKSMAN: {6: 1},
    }
    modifier_table = {
        Modifier.PISTOL_ACCURACY: {1: 0.04, 2: 0.07, 3: 0.10, 4: 0.13, 5: 0.16},
        Modifier.PISTOL_DAMAGE: {1: 0.02, 2: 0.04, 3: 0.06, 4: 0.08, 5: 0.10, 6: 0.12},
        Modifier.BARRIER_HASTE: haste,
        Modifier.LIFT_HASTE: haste,
        Modifier.STASIS_HASTE: haste,
        Modifier.THROW_HASTE: haste,
        Modifier.FIRST_AID_HASTE: haste,
        Modifier.NEURAL_SHOCK_HASTE: haste,
        Modifier.OVERLOAD_HASTE: haste,
        Modifier.SABOTAGE_HASTE: haste,
    }


class SentinelBastion(Sentinel):

    name = "Bastion"
    bastion_haste = {**Sentinel.haste, 7: 0.13, 8: 0.15, 9: 0.17, 10: 0.19, 11: 0.21, 12: 0.28}
    ability_table = {
        **Sentinel.ability_table,
        Specialization.BARRIER: {9: True},
        Specialization.STASIS: {12: True},
    }
    modifier_table = {
        **Sentinel.modifier_table,
        Modifier.PISTOL_ACCURACY: {**Sentinel.modifier_table[Modifier.PISTOL_ACCURACY], 12: 0.23},
        Modifier.BARRIER_HASTE: bastion_haste,
        Modifier.LIFT_HASTE: bastion_haste,
        Modifier.STASIS_HASTE: bastion_haste,
        Modifier.THROW_HASTE: bastion_haste,
    }


class SentinelMedic(Sentinel):

    name = "Medic"
    haste = {**Sentinel.haste, 7: 0.15}
    medic_haste = {**Sentinel.haste, 7: 0.15, 8: 0.18, 9: 0.21, 10: 0.24, 11: 0.27, 12: 0.30}
    ability_table = {
        **Sentinel.ability_table,
        Specialization.NEURAL_SHOCK: {9: True},
        Specialization.FIRST_AID: {12: True},
    }
    modifier_table = {
        **Sentinel.modifier_table,
        Modifier.BARRIER_HASTE: haste,
        Modifier.LIFT_HASTE: haste,
        Modifier.STASIS_HASTE: haste,
        Modifier.THROW_HASTE: haste,
        Modifier.OVERLOAD_HASTE: haste,
        Modifier.SABOTAGE_HASTE: haste,
        Modifier.FIRST_AID_HASTE: medic_haste,
        Modifier.NEURAL_SHOCK_HASTE: medic_haste,
    }


class Shotguns(Talent):

    name = "Shotguns"
    ability_table = {
        AbilityLevel.CARNAGE: {4: 1, 8: 2, 12: 3},
    }
    modifier_table = {
        Modifier.SHOTGUN_ACCURACY: {1: 0.10, 2: 0.14, 3: 0.17, 5: 0.20, 6: 0.22, 7: 0.24, 9: 0.26, 10: 0.28, 11: 0.30,},
        Modifier.SHOTGUN_DAMAGE:   {1: 0.05, 2: 0.08, 3: 0.10, 5: 0.12, 6: 0.14, 7: 0.16, 9: 0.18, 10: 0.19, 11: 0.20,},
    }


class Singularity(Talent):

    name = "Singularity"
    ability_table = {
        AbilityLevel.SINGULARITY: {1: 1, 7: 2, 12: 3},
    }
    modifier_table = {
        BaseValue.SINGULARITY_RADIUS: {1: 4, 2: 4.25, 3: 4.5, 4: 5.0, 6: 5.25, 7: 6.25, 8: 6.5, 9: 6.75, 10: 7.0, 11: 7.25, 12: 8.25},
    }


class Soldier(Talent):

    name = "Soldier"
    modifier_table = {
        Modifier.HEALTH: {1: 0.04, 2: 0.06, 3: 0.08, 4: 0.10, 5: 0.12, 6: 0.14},
        Modifier.HEALTH_REGEN: {1: 3.0, 2: 3.5, 3: 4.0, 4: 4.5, 5: 5.0, 6: 5.5},
    }


class SoldierCommando(Soldier):

    name = "Commando"
    weapon_damage = {7: 0.06, 8: 0.09, 9: 0.12, 10: 0.15, 11: 0.18, 12: 0.21}
    ability_table = {
        Specialization.IMMUNITY: {9: True},
        Specialization.ASSASSINATION: {12: True},
    }
    modifier_table = {
        **Soldier.modifier_table,
        Modifier.ASSAULT_RIFLE_DAMAGE: weapon_damage,
        Modifier.PISTOL_DAMAGE: weapon_damage,
        Modifier.SHOTGUN_DAMAGE: weapon_damage,
        Modifier.SNIPER_RIFLE_DAMAGE: weapon_damage,
    }


class SoldierShockTrooper(Soldier):

    name = "Shock Trooper"
    ability_table = {
        Specialization.IMMUNITY: {9: True},
        Specialization.ADRENALINE_BURST: {12: True},
    }
    modifier_table = {
        **Soldier.modifier_table,
        Modifier.DAMAGE_PROTECTION: {7: 0.06, 8: 0.08, 9: 0.10, 10: 0.12, 11: 0.14, 12: 0.16},
        Modifier.HEALTH: {**Soldier.modifier_table[Modifier.HEALTH], 7: 0.18, 8: 0.20, 9: 0.22, 10: 0.24, 11: 0.26, 12: 0.28},
    }


class SniperRifles(Talent):

    name = "Sniper Rifles"
    ability_table = {
        AbilityLevel.ASSASSINATION: {4: 1, 8: 2, 12: 3},
    }
    modifier_table = {
        Modifier.SNIPER_RIFLE_ACCURACY: {1: 0.10, 2: 0.14, 4: 0.17, 5: 0.20, 6: 0.22, 7: 0.24, 9: 0.26, 10: 0.28, 11: 0.30,},
        Modifier.SNIPER_RIFLE_DAMAGE:   {1: 0.05, 2: 0.08, 4: 0.10, 5: 0.12, 6: 0.14, 7: 0.16, 9: 0.18, 10: 0.19, 11: 0.20,},
    }


class SpectreTraining(Talent):

    name = "Spectre Training"
    ability_table = {
        AbilityLevel.UNITY: {4: 1, 8: 2, 12: 3},
    }
    modifier_table = {
        Modifier.ACCURACY_REGEN: {1: 0.004, 2: 0.006, 3: 0.008, 5: 0.01, 6: 0.012, 7: 0.014, 9: 0.016, 10: 0.018, 11: 0.02},
        Modifier.ALL_DAMAGE:   {1: 0.01, 2: 0.015, 3: 0.02, 5: 0.025, 6: 0.03, 7: 0.035, 9: 0.04, 10: 0.045, 11: 0.05},
        Modifier.ALL_DURATIONS: {1: 0.01, 2: 0.015, 3: 0.02, 5: 0.025, 6: 0.03, 7: 0.035, 9: 0.04, 10: 0.045, 11: 0.05},
        Modifier.HEALTH: {1: 0.05, 2: 0.055, 3: 0.06, 5: 0.065, 6: 0.07, 7: 0.075, 9: 0.08, 10: 0.085, 11: 0.09},
        Modifier.MAX_ACCURACY: {1: 0.02, 2: 0.03, 3: 0.04, 5: 0.05, 6: 0.06, 7: 0.07, 9: 0.08, 10: 0.09, 11: 0.10},
    }


class Stasis(Talent):

    name = "Stasis"
    ability_table = {
        AbilityLevel.STASIS: {1: 1, 6: 2, 12: 3},
    }
    modifier_table = {
        BaseValue.STASIS_DURATION: {1: 12.5, 2: 13, 3: 13.5, 4: 14, 5: 14.5, 6: 17, 7: 17.5, 8: 18, 9: 18.5, 10: 19, 11: 19.5, 12: 21},
    }


class TacticalArmor(Talent):

    name = "Tactical Armor"
    ability_table = {
        AbilityLevel.SHIELD_BOOST: {3: 1, 8: 2, 12: 3},
    }
    modifier_table = {
        Modifier.MED_ARMOR_DR:        {1: 0.05, 2: 0.08, 4: 0.10, 5: 0.12, 6: 0.14, 7: 0.16, 9: 0.18, 10: 0.19, 11: 0.20},
        Modifier.MED_ARMOR_HARDENING: {1: 0.05, 2: 0.08, 4: 0.10, 5: 0.12, 6: 0.14, 7: 0.16, 9: 0.18, 10: 0.19, 11: 0.20},
    }


class Throw(Talent):

    name = "Throw"
    ability_table = {
        AbilityLevel.THROW: {1: 1, 8: 2, 12: 3},
    }
    modifier_table = {
        BaseValue.THROW_FORCE: {1: 600, 2: 650, 3: 700, 4: 750, 5: 800, 6: 850, 7: 900, 8: 1000, 9: 1050, 10: 1100, 11: 1150, 12: 1250},
    }


class Vanguard(Talent):

    name = "Vanguard"
    modifier_table = {
        Modifier.BIOTIC_PROTECTION: {1: 0.06, 2: 0.09, 3: 0.12, 4: 0.15, 5: 0.18, 6: 0.21},
        Modifier.PISTOL_DAMAGE:  {1: 0.05, 2: 0.06, 3: 0.07, 4: 0.08, 5: 0.09, 6: 0.10},
        Modifier.SHOTGUN_DAMAGE: {1: 0.05, 2: 0.06, 3: 0.07, 4: 0.08, 5: 0.09, 6: 0.10},
    }


class VanguardNemesis(Vanguard):

    name = "Nemesis"
    nemesis_bonus = {7: 0.04, 8: 0.06, 9: 0.08, 10: 0.10, 11: 0.12, 12: 0.14}
    ability_table = {
        Specialization.WARP: {9: True},
        Specialization.LIFT: {12: True},
    }
    modifier_table = {
        **Vanguard.modifier_table,
        Modifier.THROW_DAMAGE: nemesis_bonus,
        Modifier.THROW_FORCE: nemesis_bonus,
        Modifier.BARRIER_DURATION: nemesis_bonus,
        Modifier.LIFT_DURATION: nemesis_bonus,
        Modifier.WARP_DURATION: nemesis_bonus,        
    }


class VanguardShockTrooper(Vanguard):

    name = "Shock Trooper"
    ability_table = {
        Specialization.BARRIER: {9: True},
        Specialization.ADRENALINE_BURST: {12: True},
    }
    modifier_table = {
        **Vanguard.modifier_table,
        Modifier.HEALTH: {7: 0.04, 8: 0.06, 9: 0.08, 10: 0.10, 11: 0.12, 12: 0.14},
        Modifier.DAMAGE_PROTECTION: {7: 0.06, 8: 0.08, 9: 0.10, 10: 0.12, 11: 0.14, 12: 0.16},
    }


class Warp(Talent):

    name = "Warp"
    ability_table = {
        AbilityLevel.WARP: {1: 1, 6: 2, 12: 3},
    }
    modifier_table = {
        BaseValue.WARP_DURATION: {1: 7, 2: 8, 3: 9, 4: 10, 5: 11, 6: 13, 7: 14, 8: 15, 9: 16, 10: 17, 11: 18, 12: 20},
    }
