from enums import AbilityLevel, AbilitySpec, Modifier

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
    modifier_table = {
        Modifier.BIOTIC_HASTE: {1: 0.04, 2: 0.06, 3: 0.08, 4: 0.10, 5: 0.12, 6: 0.14},
        Modifier.BIOTIC_PROTECTION: {1: 0.06, 2: 0.09, 3: 0.12, 4: 0.15, 5: 0.18, 6: 0.21},
    }


class AdeptBastion(Adept):

    name = "Bastion"
    ability_table = {}
    modifier_table = {}


class AdeptNemesis(Adept):

    name = "Nemesis"
    ability_table = {}
    modifier_table = {}


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
    ability_table = {
        AbilityLevel.ADRENALINE_BURST: {3: 1, 8: 2, 12: 3},
    }
    modifier_table = {
        Modifier.MELEE_DAMAGE:  {1: 0.30, 2: 0.35, 4: 0.40, 5: 0.44, 6: 0.48, 7: 0.52, 9: 0.56, 10: 0.60, 11: 0.64},
        Modifier.WEAPON_DAMAGE: {1: 0.01, 2: 0.02, 4: 0.03, 5: 0.04, 6: 0.05, 7: 0.06, 9: 0.07, 10: 0.08, 11: 0.09},
    }


class Barrier(Talent):

    name = "Barrier"
    ability_table = {
        AbilityLevel.BARRIER: {1: 1, 7: 2, 12: 3},
    }
    modifier_table = {
        Modifier.BARRIER_DURATION: {1: 10.0, 2: 10.5, 3: 11.0, 4: 11.5, 5: 12.0, 6: 12.5, 7: 16.5, 8: 17.0, 9: 17.5, 10: 18.0, 11: 18.5, 12: 23.0},
        Modifier.BARRIER_SHIELDING: {1: 400, 2: 420, 3: 440, 4: 460, 5: 480, 6: 500, 7: 700, 8: 720, 9: 740, 10: 760, 11: 780, 12: 1000},
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
    ability_table = {
        AbilityLevel.DAMPING: {1: 1, 6: 2, 12: 3},
    }
    modifier_table = {
        Modifier.TECH_MINE_RADIUS: {2: 0.10, 3: 0.14, 4: 0.18, 5: 0.20, 7: 0.22, 8: 0.24, 9: 0.26, 10: 0.28, 11: 0.30},
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
    modifier_table = {
        Modifier.TECH_HASTE: {1: 0.04, 2: 0.06, 3: 0.08, 4: 0.10, 5: 0.12, 6: 0.14},
        Modifier.TECH_PROTECTION: {1: 0.06, 2: 0.09, 3: 0.12, 4: 0.15, 5: 0.18, 6: 0.21},
    }


class EngineerMedic(Engineer):

    name = "Medic"
    ability_table = {}
    modifier_table = {}


class EngineerOperative(Engineer):

    name = "Operative"
    ability_table = {}
    modifier_table = {}


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
    ability_table = {
        AbilityLevel.AI_HACKING: {1: 1, 7: 2, 12: 3},
    }
    modifier_table = {
        Modifier.TECH_MINE_HASTE: {2: 0.06, 3: 0.09, 4: 0.12, 5: 0.15, 6: 0.18, 8: 0.21, 9: 0.24, 10: 0.27, 11: 0.30},
    }


class Infiltrator(Talent):

    name = "Infiltrator"
    modifier_table = {}


class InfiltratorCommando(Infiltrator):

    name = "Commando"
    ability_table = {}
    modifier_table = {}


class InfiltratorOperative(Infiltrator):

    name = "Operative"
    ability_table = {}
    modifier_table = {}


class Intimidate(Talent):

    name = "Intimidate"
    modifier_table = {}


class Lift(Talent):

    name = "Lift"
    ability_table = {
        AbilityLevel.LIFT: {1: 1, 7: 2, 12: 3},
    }
    modifier_table = {
        Modifier.LIFT_DURATION: {1: 6.0, 2: 6.4, 3: 6.8, 4: 7.2, 5: 7.6, 6: 8.0, 7: 9.0, 8: 9.4, 9: 9.8, 10: 10.2, 11: 10.6, 12: 12.0},
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
    modifier_table = {}


class SentinelBastion(Sentinel):

    name = "Bastion"
    ability_table = {}
    modifier_table = {}


class SentinelMedic(Sentinel):

    name = "Medic"
    ability_table = {}
    modifier_table = {}


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
        Modifier.SINGULARITY_RADIUS: {1: 4, 2: 4.25, 3: 4.5, 4: 5.0, 6: 5.25, 7: 6.25, 8: 6.5, 9: 6.75, 10: 7.0, 11: 7.25, 12: 8.25},
    }


class Soldier(Talent):

    name = "Soldier"
    modifier_table = {
        Modifier.HEALTH: {1: 0.04, 2: 0.06, 3: 0.08, 4: 0.10, 5: 0.12, 6: 0.14},
        Modifier.HEALTH_REGEN: {1: 3.0, 2: 3.5, 3: 4.0, 4: 4.5, 5: 5.0, 6: 5.5},
    }


class SoldierCommando(Soldier):

    name = "Commando"
    ability_table = {
        AbilitySpec.IMMUNITY: {9: True},
        AbilitySpec.ASSASSINATION: {12: True},
    }
    modifier_table = {
        **Soldier.modifier_table,
        Modifier.WEAPON_DAMAGE: {7: 0.06, 8: 0.09, 9: 0.12, 10: 0.15, 11: 0.18, 12: 0.21},
    }


class SoldierShockTrooper(Soldier):

    name = "Shock Trooper"
    ability_table = {
        AbilitySpec.IMMUNITY: {9: True},
        AbilitySpec.ADRENALINE_BURST: {12: True},
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
    ability_table = {}
    modifier_table = {}


class Stasis(Talent):

    name = "Stasis"
    ability_table = {
        AbilityLevel.STASIS: {1: 1, 6: 2, 12: 3},
    }
    modifier_table = {
        Modifier.STASIS_DURATION: {1: 12.5, 2: 13, 3: 13.5, 4: 14, 5: 14.5, 6: 17, 7: 17.5, 8: 18, 9: 18.5, 10: 19, 11: 19.5, 12: 21},
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
        Modifier.THROW_FORCE: {1: 600, 2: 650, 3: 700, 4: 750, 5: 800, 6: 850, 7: 900, 8: 1000, 9: 1050, 10: 1100, 11: 1150, 12: 1250},
    }


class Vanguard(Talent):

    name = "Vanguard"
    modifier_table = {}


class VanguardNemesis(Talent):

    name = "Nemesis"
    ability_table = {}
    modifier_table = {}


class VanguardShockTrooper(Talent):

    name = "Shock Trooper"
    ability_table = {}
    modifier_table = {}


class Warp(Talent):

    name = "Warp"
    ability_table = {
        AbilityLevel.WARP: {1: 1, 6: 2, 12: 3},
    }
    modifier_table = {
        Modifier.WARP_DURATION: {1: 7, 2: 8, 3: 9, 4: 10, 5: 11, 6: 13, 7: 14, 8: 15, 9: 16, 10: 17, 11: 18, 12: 20},
    }
