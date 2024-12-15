from enums import AbilityRank, PercentModifier

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
