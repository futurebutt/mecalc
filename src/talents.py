from enums import AbilityLevel, PercentModifier

# Rank -> Value at Rank
Lookup = dict[int, float]


class Talent:

    name: str = "<TALENT>"
    ability_table: dict[AbilityLevel, Lookup] = {}
    modifier_table: dict[PercentModifier, Lookup] = {}

    def __init__(self, rank: int):
        self.rank: int = rank
        self.modifiers: dict[PercentModifier, float] = {}
        self.ability_levels: dict[AbilityLevel, float] = {}

    def calculate_modifiers(self):
        for modifier, values in self.modifier_table.items():
            best_value = 0
            for threshold, value in values.items():
                if self.rank >= threshold:
                    best_value = value
            self.modifiers[modifier] = best_value

    def calculate_ability_levels(self):
        for ability, level_lookup in self.ability_table.items():
            best_level: int = 0
            for threshold, level in level_lookup.items():
                if self.rank >= threshold:
                    best_level = level
            self.ability_levels[ability] = best_level

    def get_modifiers(self) -> dict[PercentModifier, float]:
        self.calculate_modifiers()
        return self.modifiers

    def get_abilities(self) -> dict[AbilityLevel, int]:
        self.calculate_ability_levels()
        return self.ability_levels


class AssaultRifles(Talent):

    name = "Assault Rifles"
    ability_table = {
        AbilityLevel.OVERKILL: {1: 1, 8: 2, 12: 3},
    }
    modifier_table = {
        PercentModifier.ASSAULT_RIFLE_ACCURACY: {2: 0.10, 3: 0.14, 4: 0.17, 5: 0.20, 6: 0.22, 7: 0.24, 9: 0.26, 10: 0.28, 11: 0.30,},
        PercentModifier.ASSAULT_RIFLE_DAMAGE:   {2: 0.05, 3: 0.08, 4: 0.10, 5: 0.12, 6: 0.14, 7: 0.16, 9: 0.18, 10: 0.19, 11: 0.20,},
    }



class AssaultTraining(Talent):

    name = "Assault Training"
    ability_table = {
        AbilityLevel.ADRENALINE_BURST: {3: 1, 8: 2, 12: 3},
    }
    modifier_table = {
        PercentModifier.MELEE_DAMAGE:  {1: 0.30, 2: 0.35, 4: 0.40, 5: 0.44, 6: 0.48, 7: 0.52, 9: 0.56, 10: 0.60, 11: 0.64},
        PercentModifier.WEAPON_DAMAGE: {1: 0.01, 2: 0.02, 4: 0.03, 5: 0.04, 6: 0.05, 7: 0.06, 9: 0.07, 10: 0.08, 11: 0.09},
    }


class BasicArmor(Talent):

    name = "Basic Armor"
    ability_table = {
        AbilityLevel.SHIELD_BOOST: {3: 1, 8: 2, 12: 3},
    }
    modifier_table = {
        PercentModifier.LIGHT_ARMOR_DR:        {1: 0.05, 2: 0.08, 4: 0.10, 5: 0.12, 6: 0.14, 7: 0.16, 9: 0.18, 10: 0.19, 11: 0.20},
        PercentModifier.LIGHT_ARMOR_HARDENING: {1: 0.05, 2: 0.08, 4: 0.10, 5: 0.12, 6: 0.14, 7: 0.16, 9: 0.18, 10: 0.19, 11: 0.20},
    }


class Fitness(Talent):

    name = "Fitness"
    ability_table = {
        AbilityLevel.IMMUNITY: {4: 1, 8: 2, 12: 3},
    }
    modifier_table = {
        PercentModifier.HEALTH: {1: 0.10, 2: 0.14, 3: 0.17, 5: 0.20, 6: 0.22, 7: 0.24, 9: 0.26, 10: 0.28, 11: 0.30},
    }


class Pistols(Talent):

    name = "Pistols"
    ability_table = {
        AbilityLevel.MARKSMAN: {3: 1, 8: 2, 12: 3},
    }
    modifier_table = {
        PercentModifier.PISTOL_ACCURACY: {1: 0.10, 2: 0.14, 4: 0.17, 5: 0.20, 6: 0.22, 7: 0.24, 9: 0.26, 10: 0.28, 11: 0.30,},
        PercentModifier.PISTOL_DAMAGE:   {1: 0.05, 2: 0.08, 4: 0.10, 5: 0.12, 6: 0.14, 7: 0.16, 9: 0.18, 10: 0.19, 11: 0.20,},
    }


class Shotguns(Talent):
    name = "Shotguns"
    ability_table = {
        AbilityLevel.CARNAGE: {4: 1, 8: 2, 12: 3},
    }
    modifier_table = {
        PercentModifier.SHOTGUN_ACCURACY: {1: 0.10, 2: 0.14, 3: 0.17, 5: 0.20, 6: 0.22, 7: 0.24, 9: 0.26, 10: 0.28, 11: 0.30,},
        PercentModifier.SHOTGUN_DAMAGE:   {1: 0.05, 2: 0.08, 3: 0.10, 5: 0.12, 6: 0.14, 7: 0.16, 9: 0.18, 10: 0.19, 11: 0.20,},
    }


class SniperRifles(Talent):
    name = "Sniper Rifles"
    ability_table = {
        AbilityLevel.ASSASSINATION: {4: 1, 8: 2, 12: 3},
    }
    modifier_table = {
        PercentModifier.SNIPER_RIFLE_ACCURACY: {1: 0.10, 2: 0.14, 4: 0.17, 5: 0.20, 6: 0.22, 7: 0.24, 9: 0.26, 10: 0.28, 11: 0.30,},
        PercentModifier.SNIPER_RIFLE_DAMAGE:   {1: 0.05, 2: 0.08, 4: 0.10, 5: 0.12, 6: 0.14, 7: 0.16, 9: 0.18, 10: 0.19, 11: 0.20,},
    }

