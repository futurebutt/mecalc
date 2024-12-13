from enums import BaseValue, BonusValue, Feature


Lookup = dict[int, int | float | bool]
BonusTable = dict[BonusValue, Lookup]


class Talent:

    bonus_table: BonusTable = {}

    def __init__(self, rank: int):
        self.rank: int = rank
        self.bonuses: dict[BonusValue, float] = {}

    def calculate_bonuses(self):
        for bonus_type, lookup in self.bonus_table.items():
            best_bonus: float = 0
            for threshold, value in lookup.items():
                if self.rank >= threshold:
                    best_bonus = value
            self.bonuses[bonus_type] = best_bonus

    def get_bonuses(self) -> dict[BonusValue, float]:
        self.calculate_bonuses()
        return dict(self.bonuses)


class Specialization:

    spec_table: BonusTable = {}


def combine_bonus_tables(table_1: BonusTable, table_2: BonusTable) -> BonusTable:

    combined: BonusTable = {}

    for bonus_type, levels in table_1.items():
        if bonus_type not in combined:
            combined[bonus_type] = levels.copy()
        else:
            combined[bonus_type].update(levels)

    for bonus_type, levels in table_2.items():
        if bonus_type not in combined:
            combined[bonus_type] = levels.copy()
        else:
            combined[bonus_type].update(levels)

    return combined


class TalentAssaultTraining(Talent):

    bonus_table = {
        BonusValue.AR_DAMAGE:      {1: 0.01, 2: 0.02, 4: 0.03, 5: 0.04, 6: 0.05, 7: 0.06, 9: 0.07, 10: 0.08, 11: 0.09},
        BonusValue.PISTOL_DAMAGE:  {1: 0.01, 2: 0.02, 4: 0.03, 5: 0.04, 6: 0.05, 7: 0.06, 9: 0.07, 10: 0.08, 11: 0.09},
        BonusValue.SHOTGUN_DAMAGE: {1: 0.01, 2: 0.02, 4: 0.03, 5: 0.04, 6: 0.05, 7: 0.06, 9: 0.07, 10: 0.08, 11: 0.09},
        BonusValue.SR_DAMAGE:      {1: 0.01, 2: 0.02, 4: 0.03, 5: 0.04, 6: 0.05, 7: 0.06, 9: 0.07, 10: 0.08, 11: 0.09},
        BonusValue.MELEE_DAMAGE:   {1: 0.30, 2: 0.35, 4: 0.40, 5: 0.44, 6: 0.48, 7: 0.52, 9: 0.56, 10: 0.60, 11: 0.64},
        BaseValue.ADRENALINE_COOLDOWN: {3: 120, 8: 90, 12: 45},
        BaseValue.ADRENALINE_ACC_COST: {3: 0.30}
    }


class TalentFitness(Talent):

    bonus_table = {
        BonusValue.HEALTH: {1: 0.10, 2: 0.14, 3: 0.17, 5: 0.20, 6: 0.22, 7: 0.24, 9: 0.26, 10: 0.28, 11: 0.30},
        BaseValue.IMMUNITY_DR: {4: 0.75, 8: 0.85, 12: 0.90},
        BaseValue.IMMUNITY_DURATION: {4: 6},
        BaseValue.IMMUNITY_COOLDOWN: {4: 45}
    }


class TalentAssaultRifles(Talent):

    bonus_table = {
        BonusValue.AR_DAMAGE:   {2: 0.05, 3: 0.08, 4: 0.10, 5: 0.12, 6: 0.14, 7: 0.16, 9: 0.18, 10: 0.19, 11: 0.20},
        BonusValue.AR_ACCURACY: {2: 0.10, 3: 0.14, 4: 0.17, 5: 0.20, 6: 0.22, 7: 0.24, 9: 0.26, 10: 0.28, 11: 0.30},
        BaseValue.OVERKILL_HEAT_DOWN:    {1: 0.80, 8: 0.90, 12: 1.00},
        BaseValue.OVERKILL_DAMAGE_BONUS: {1: 0.50, 8: 0.75, 12: 1.00},
        BaseValue.OVERKILL_DURATION: {1: 6},
        BaseValue.OVERKILL_COOLDOWN: {1: 45}
    }


class TalentPistols(Talent):

    bonus_table = {
        BonusValue.PISTOL_DAMAGE:   {1: 0.05, 2: 0.08, 4: 0.10, 5: 0.12, 6: 0.14, 7: 0.16, 9: 0.18, 10: 0.19, 11: 0.20},
        BonusValue.PISTOL_ACCURACY: {1: 0.10, 2: 0.14, 4: 0.17, 5: 0.20, 6: 0.22, 7: 0.24, 9: 0.26, 10: 0.28, 11: 0.30},
        BaseValue.MARKSMAN_ACC_BONUS: {3: 0.60},
        BaseValue.MARKSMAN_DAMAGE_BONUS:   {3: 0.25, 8: 0.50, 12: 0.75},
        BaseValue.MARKSMAN_HEADSHOT_BONUS: {3: 0.50, 8: 0.75, 12: 1.00},
        BaseValue.MARKSMAN_DURATION: {3: 6},
        BaseValue.MARKSMAN_COOLDOWN: {3: 45}
    }


class TalentShotguns(Talent):

    bonus_table = {
        BonusValue.SHOTGUN_DAMAGE:   {1: 0.05, 2: 0.08, 3: 0.10, 5: 0.12, 6: 0.14, 7: 0.16, 9: 0.18, 10: 0.19, 11: 0.20},
        BonusValue.SHOTGUN_ACCURACY: {1: 0.10, 2: 0.14, 3: 0.17, 5: 0.20, 6: 0.22, 7: 0.24, 9: 0.26, 10: 0.28, 11: 0.30},
        BaseValue.CARNAGE_DPS_MULT: {4: 2.00, 8: 2.25, 12: 2.50},
        BaseValue.CARNAGE_RADIUS: {4: 2, 8: 2.5, 12: 3},
        BaseValue.CARNAGE_DURATION: {4: 6},
        BaseValue.CARNAGE_COOLDOWN: {4: 45}
    }


class TalentSniperRifles(Talent):

    bonus_table = {
        BonusValue.SR_DAMAGE:   {1: 0.05, 2: 0.08, 4: 0.10, 5: 0.12, 6: 0.14, 7: 0.16, 9: 0.18, 10: 0.19, 11: 0.20},
        BonusValue.SR_ACCURACY: {1: 0.10, 2: 0.14, 4: 0.17, 5: 0.20, 6: 0.22, 7: 0.24, 9: 0.26, 10: 0.28, 11: 0.30},
        BaseValue.ASSASSIN_DPS_MULT: {3: 2.00, 8: 2.50, 12: 3.00},
        BaseValue.ASSASSIN_DURATION: {3: 6},
        BaseValue.ASSASSIN_COOLDOWN: {3: 45}
    }


# Hardening and damage reduction scale identically with all armor-type talents.
_ARMOR_LOOKUP: Lookup = {1: 0.05, 2: 0.08, 4: 0.10, 5: 0.12, 6: 0.14, 7: 0.16, 9: 0.18, 10: 0.19, 11: 0.20}

# Shield boost is the same wherever you unlock it.
_SHIELD_BOOST_TABLE: BonusTable = {
    BaseValue.SHIELD_BOOST_SPS: {3: 0.30, 8: 0.40, 12: 0.50},
    BaseValue.SHIELD_BOOST_DURATION: {3: 2},
    BaseValue.SHIELD_BOOST_COOLDOWN: {3: 45},
    BaseValue.SHIELD_BOOST_ACC_COST: {3: 0.30}
}


class TalentBasicArmor(Talent):

    bonus_table = {
        BonusValue.LIGHT_DR: _ARMOR_LOOKUP,
        BonusValue.LIGHT_HARDENING: _ARMOR_LOOKUP,
        **_SHIELD_BOOST_TABLE,
    }


class TalentCombatArmor(Talent):

    bonus_table = {
        BonusValue.HEAVY_DR: _ARMOR_LOOKUP,
        BonusValue.HEAVY_HARDENING: _ARMOR_LOOKUP,
        **_SHIELD_BOOST_TABLE,
    }


class TalentTacticalArmor(Talent):

    bonus_table = {
        BonusValue.MED_DR: _ARMOR_LOOKUP,
        BonusValue.MED_HARDENING: _ARMOR_LOOKUP,
        **_SHIELD_BOOST_TABLE,
    }


class TalentDecryption(Talent):

    techmine_damage: Lookup = {2: 0.10, 3: 0.14, 4: 0.18, 6: 0.20, 7: 0.22, 8: 0.24, 10: 0.26, 11: 0.28, 12: 0.30}

    bonus_table = {
        BonusValue.SABOTAGE_DAMAGE: techmine_damage,
        BonusValue.OVERLOAD_DAMAGE: techmine_damage,
        BonusValue.DAMPING_DAMAGE: techmine_damage,
        BaseValue.SABOTAGE_DAMAGE: {1: 50, 5: 100, 9: 150},
        BaseValue.SABOTAGE_DPS: {1: 2, 5: 3, 9: 4},  # TODO: does the techmine damage bonus apply to this?
        BaseValue.SABOTAGE_DURATION: {1: 15, 5: 20, 9: 25},
        BaseValue.SABOTAGE_COOLDOWN: {1: 60, 5: 50, 9: 40},
        BaseValue.SABOTAGE_ACC_COST: {1: 0.60},
    }


class TalentElectronics(Talent):

    bonus_table = {
        BonusValue.SHIELD_CAPACITY: {2: 30, 3: 60, 4: 90, 6: 120, 7: 150, 8: 180, 10: 210, 11: 240, 12: 270},
        BonusValue.HULL_REPAIR: {2: 400, 3: 600, 4: 800, 6: 1200, 7: 1400, 8: 1600, 10: 2000, 11: 2200, 12: 2400},
        BaseValue.OVERLOAD_DAMAGE: {1: 50, 5: 100, 9: 150},
        BaseValue.OVERLOAD_SHIELD_DAMAGE: {1: 200, 5: 400, 9: 600},
        BaseValue.OVERLOAD_DR_DOWN: {1: 0.20, 5: 0.25, 9: 0.30},
        BaseValue.OVERLOAD_DURATION: {1: 10},
        BaseValue.OVERLOAD_COOLDOWN: {1: 60, 5: 50, 9: 40},
        BaseValue.OVERLOAD_ACC_COST: {1: 0.60},
    }


class TalentHacking(Talent):

    techmine_haste: Lookup = {2: 0.06, 3: 0.09, 4: 0.12, 5: 0.15, 6: 0.18, 8: 0.21, 9: 0.24, 10: 0.27, 11: 0.30}

    bonus_table = {
        BonusValue.SABOTAGE_HASTE: techmine_haste,
        BonusValue.OVERLOAD_HASTE: techmine_haste,
        BonusValue.DAMPING_HASTE: techmine_haste,
        BaseValue.AI_HACK_DURATION: {1: 20, 7: 25, 12: 30},
        BaseValue.AI_HACK_COOLDOWN: {1: 60, 7: 50, 12: 40},
        BaseValue.AI_HACK_ACC_COST: {1: 0.80},
    }


class TalentDamping(Talent):

    techmine_radius: Lookup = {2: 0.10, 3: 0.14, 4: 0.18, 5: 0.20, 7: 0.22, 8: 0.24, 9: 0.26, 10: 0.28, 11: 0.30}

    bonus_table = {
        BonusValue.SABOTAGE_RADIUS: techmine_radius,
        BonusValue.OVERLOAD_RADIUS: techmine_radius,
        BonusValue.DAMPING_RADIUS: techmine_radius,
        BaseValue.DAMPING_DAMAGE: {1: 50, 6: 100},
        BaseValue.DAMPING_STUN: {1: 3},
        BaseValue.DAMPING_ENEMY_COOLDOWN: {1: 0.30, 6: 0.45, 12: 0.60},
        BaseValue.DAMPING_COOLDOWN: {1: 60, 6: 50, 12: 40},
        BaseValue.DAMPING_ACC_COST: {1: 0.60},
    }


class TalentBarrier(Talent):

    bonus_table = {
        BaseValue.BARRIER_STRENGTH: {1: 400, 2: 420, 3: 440, 4: 460, 5: 480, 6: 500, 7: 700, 8: 720, 9: 740, 10: 760, 11: 780, 12: 1000},
        BaseValue.BARRIER_DURATION: {1: 10, 2: 10.5, 3: 11, 4: 11.5, 5: 12, 6: 12.5, 7: 16.5, 8: 17, 9: 17.5, 10: 18, 11: 18.5, 12: 23},
        BaseValue.BARRIER_COOLDOWN: {1: 60, 7: 50, 12: 40},
        BaseValue.BARRIER_ACC_COST: {1: 0.80},
        BaseValue.BARRIER_REGEN: {1: 0},
    }


class TalentLift(Talent):

    bonus_table = {
        BaseValue.LIFT_RADIUS: {1: 4, 7: 5, 12: 6},
        BaseValue.LIFT_DURATION: {1: 6, 2: 6.4, 3: 6.8, 4: 7.2, 5: 7.6, 6: 8, 7: 9, 8: 9.4, 9: 9.8, 10: 10.2, 11: 10.6, 12: 12},
        BaseValue.LIFT_COOLDOWN: {1: 60, 7: 50, 12: 40},
        BaseValue.LIFT_ACC_COST: {1: 0.80, 7: 0.60, 12: 0.40}
    }


class TalentSingularity(Talent):

    bonus_table = {
        BaseValue.SINGULARITY_RADIUS: {1: 4, 2: 4.25, 3: 4.5, 4: 4.75, 5: 5, 6: 5.25, 7: 6.25, 8: 6.5, 9: 6.75, 10: 7, 11: 7.25, 12: 8.25},
        BaseValue.SINGULARITY_DURATION: {1: 4, 7: 6, 12: 8},
        BaseValue.SINGULARITY_COOLDOWN: {1: 60, 7: 50, 12: 40},
        BaseValue.SINGULARITY_ACC_COST: {1: 0.80}
    }


class TalentStasis(Talent):

    bonus_table = {
        BaseValue.STASIS_DURATION: {1: 12.5, 2: 13, 3: 13.5, 4: 14, 5: 14.5, 6: 17, 7: 17.5, 8: 18, 9: 18.5, 10: 19, 11: 19.5, 12: 21},
        BaseValue.STASIS_COOLDOWN: {1: 60, 6: 50, 12: 40},
        BaseValue.STASIS_ACC_COST: {1: 0.80},
        Feature.STASIS_ENABLE_DAMAGE: {1: False},
    }


class TalentThrow(Talent):

    bonus_table = {
        BaseValue.THROW_FORCE: {1: 600, 2: 650, 3: 700, 4: 750, 5: 800, 6: 850, 7: 900, 8: 1000, 9: 1050, 10: 1100, 11: 1150, 12: 1250},
        BaseValue.THROW_RADIUS: {1: 4, 8: 5, 12: 6},
        BaseValue.THROW_COOLDOWN: {1: 60, 8: 50, 12: 40},
        BaseValue.THROW_ACC_COST: {1: 0.60, 8: 0.45, 12: 0.30}
    }


class TalentWarp(Talent):

    bonus_table = {
        BaseValue.WARP_DPS: {1: 6, 6: 8, 12: 10},
        BaseValue.WARP_DR_DOWN: {1: 0.50, 6: 0.60, 12: 0.75},
        BaseValue.WARP_RADIUS: {1: 4, 6: 5, 12: 6},
        BaseValue.WARP_DURATION: {},
        BaseValue.WARP_COOLDOWN: {1: 60, 6: 50, 12: 40},
        BaseValue.WARP_ACC_COST: {1: 80}
    }


class TalentFirstAid(Talent):

    bonus_table = {
        BonusValue.FIRST_AID_HEALING: {1: 40, 2: 50, 3: 60, 4: 70, 5: 80, 6: 100, 7: 110, 8: 120, 9: 130, 10: 140, 11: 150, 12: 180}
    }


class TalentMedicine(Talent):

    bonus_table = {
        BonusValue.FIRST_AID_HASTE: {2: 0.10, 3: 0.14, 4: 0.17, 5: 0.20, 6: 0.22, 8: 0.24, 9: 0.26, 10: 0.28, 11: 0.30},
        BaseValue.NEURAL_SHOCK_DAMAGE: {1: 40, 7: 80, 12: 120},
        BaseValue.NEURAL_SHOCK_KNOCKOUT: {1: 1, 7: 3, 12: 5},
        BaseValue.NEURAL_SHOCK_COOLDOWN: {1: 45},
        BaseValue.NEURAL_SHOCK_ACC_COST: {1: 0.60},
    }


class TalentCharm(Talent):

    bonus_table = {
        BonusValue.STORE_DISCOUNT: {4: 0.02, 8: 0.05, 12: 0.08}
    }


class TalentIntimidate(Talent):

    bonus_table = {
        BonusValue.SALE_BONUS: {4: 0.02, 8: 0.05, 12: 0.08}
    }


class TalentSpectreTraining:

    bonus_table = {
        BonusValue.ALL_DAMAGE:    {1: 0.010, 2: 0.015, 3: 0.020, 5: 0.025, 6: 0.030, 7: 0.035, 9: 0.040, 10: 0.045, 11: 0.050},
        BonusValue.ALL_DURATIONS: {1: 0.050, 2: 0.055, 3: 0.060, 5: 0.065, 6: 0.070, 7: 0.075, 9: 0.080, 10: 0.085, 11: 0.090},
        BonusValue.MAX_ACCURACY: {1: 0.02, 2: 0.03, 3: 0.04, 5: 0.05, 6: 0.06, 7: 0.07, 9: 0.08, 10: 0.09, 11: 0.10},
        BonusValue.ACCURACY_REGEN: {1: 0.004, 2: 0.006, 3: 0.008, 5: 0.010, 6: 0.012, 7: 0.014, 9: 0.016, 10: 0.018, 11: 0.020},
        BaseValue.UNITY_HEALTH: {4: 0.15, 8: 0.20, 12: 0.30},
        BaseValue.UNITY_SHIELDS: {4: 0.40, 8: 0.60, 12: 1.00},
        BaseValue.UNITY_COOLDOWN: {4: 150, 8: 120, 12: 90},
        BaseValue.UNITY_ACC_COST: {4: 0.45}
    }


class TalentAdept(Talent):

    adept_haste: dict[int, float] = {1: 0.04, 2: 0.06, 3: 0.08, 4: 0.10, 5: 0.12, 6: 0.14}

    bonus_table = {
        BonusValue.THROW_HASTE: adept_haste,
        BonusValue.LIFT_HASTE: adept_haste,
        BonusValue.WARP_HASTE: adept_haste,
        BonusValue.SINGULARITY_HASTE: adept_haste,
        BonusValue.BARRIER_HASTE: adept_haste,
        BonusValue.STASIS_HASTE: adept_haste,
        BonusValue.BIOTIC_PROTECTION: {1: 0.06, 2: 0.09, 3: 0.12, 4: 0.15, 5: 0.18, 6: 0.21},
    }


class TalentAdeptBastion(TalentAdept, Specialization):

    bastion_haste: dict[int, float] = {7: 0.18, 8: 0.20, 9: 0.22, 10: 0.24, 11: 0.26, 12: 0.28}

    spec_table = {
        BonusValue.THROW_HASTE: bastion_haste,
        BonusValue.LIFT_HASTE: bastion_haste,
        BonusValue.WARP_HASTE: bastion_haste,
        BonusValue.SINGULARITY_HASTE: bastion_haste,
        BonusValue.BARRIER_HASTE: bastion_haste,
        BonusValue.STASIS_HASTE: bastion_haste,
        BonusValue.BARRIER_STRENGTH: {9: 0.25},
        BonusValue.BARRIER_DURATION: {9: 0.25},
        BonusValue.BARRIER_REGEN: {9: 40},
        Feature.STASIS_ENABLE_DAMAGE: {12, True}
    }

    bonus_table = combine_bonus_tables(TalentAdept.bonus_table, spec_table)


class TalentAdeptNemesis(TalentAdept, Specialization):

    nemesis_bonus: dict[int, float] = {7: 0.04, 8: 0.06, 9: 0.08, 10: 0.10, 11: 0.12, 12: 0.14}

    spec_table = {
        BonusValue.THROW_FORCE: nemesis_bonus,
        BonusValue.LIFT_DURATION: nemesis_bonus,
        BonusValue.WARP_DURATION: nemesis_bonus,
        BonusValue.SINGULARITY_DURATION: nemesis_bonus,
        BonusValue.BARRIER_DURATION: nemesis_bonus,
        BonusValue.STASIS_DURATION: nemesis_bonus,
    }

    bonus_table = combine_bonus_tables(TalentAdept.bonus_table, spec_table)


class TalentEngineer(Talent):

    engineer_haste: Lookup = {1: 0.04, 2: 0.06, 3: 0.08, 4: 0.10, 5: 0.12, 6: 0.14}

    bonus_table = {
        BonusValue.SABOTAGE_HASTE: engineer_haste,
        BonusValue.OVERLOAD_HASTE: engineer_haste,
        BonusValue.DAMPING_HASTE: engineer_haste,
        BonusValue.HACKING_HASTE: engineer_haste,
        BonusValue.NEURAL_SHOCK_HASTE: engineer_haste,
        BonusValue.FIRST_AID_HASTE: engineer_haste,
        BonusValue.TECH_PROTECTION: {1: 0.06, 2: 0.09, 3: 0.12, 4: 0.15, 5: 0.18, 6: 0.21}
    }


class TalentEngineerMedic(TalentEngineer, Specialization):

    medic_haste: Lookup = {7: 0.20, 8: 0.23, 9: 0.26, 10: 0.29, 11: 0.32, 12: 0.35}
    lvl_7_haste: Lookup = {7, medic_haste[7]}

    spec_table = {
        BonusValue.SABOTAGE_HASTE: lvl_7_haste,
        BonusValue.OVERLOAD_HASTE: lvl_7_haste,
        BonusValue.DAMPING_HASTE: lvl_7_haste,
        BonusValue.HACKING_HASTE: lvl_7_haste,
        BonusValue.NEURAL_SHOCK_HASTE: lvl_7_haste,
        BonusValue.FIRST_AID_HASTE: medic_haste,
        BonusValue.NEURAL_SHOCK_HASTE: medic_haste,
        BonusValue.NEURAL_SHOCK_DURATION: {9, 0.25},
        BonusValue.NEURAL_SHOCK_DAMAGE: {9, 40},
        BonusValue.FIRST_AID_HEALING: {12, 80},
        Feature.FIRST_AID_IGNORES_TOXIC: {12, True},
        Feature.FIRST_AID_REVIVES: {12, True},
    }

    bonus_table = combine_bonus_tables(TalentEngineer.bonus_table, spec_table)


class TalentEngineerOperative(TalentEngineer, Specialization):

    operative_haste: Lookup = {7: 0.18, 8: 0.20, 9: 0.22, 10: 0.24, 11: 0.26, 12: 0.28}

    spec_table = {
        BonusValue.DAMPING_HASTE: operative_haste,
        BonusValue.FIRST_AID_HASTE: operative_haste,
        BonusValue.HACKING_HASTE: operative_haste,
        BonusValue.NEURAL_SHOCK_HASTE: operative_haste,
        BonusValue.OVERLOAD_HASTE: operative_haste,
        BonusValue.SABOTAGE_HASTE: operative_haste,
        # Overload Specialization
        BonusValue.OVERLOAD_RADIUS: {9, 2},
        BonusValue.OVERLOAD_DAMAGE: {9, 50},
        BonusValue.OVERLOAD_SHIELD_DAMAGE: {9, 200},
        BonusValue.OVERLOAD_DR_DOWN: {9, 0.05},
        # Sabotage Specialization
        BonusValue.SABOTAGE_RADIUS: {12, 2},
        BonusValue.SABOTAGE_DAMAGE: {12, 50},
        BonusValue.SABOTAGE_DPS: {12, 1},
        BonusValue.SABOTAGE_DURATION: {12, 5},
    }

    bonus_table = combine_bonus_tables(TalentEngineer.bonus_table, spec_table)


class TalentSoldier(Talent):

    bonus_table = {
        BonusValue.HEALTH: {1: 0.04, 2: 0.06, 3: 0.08, 4: 0.10, 5: 0.12, 6: 0.14},
        BonusValue.HEALTH_REGEN: {1: 3, 2: 3.5, 3: 4, 4: 4.5, 5: 5, 6: 5.5}
    }


class TalentSoldierCommando(TalentSoldier, Specialization):

    commando_damage: Lookup = {7: 0.06, 8: 0.09, 9: 0.12, 10: 0.15, 11: 0.18, 12: 0.21}

    spec_table = {
        BonusValue.AR_DAMAGE: commando_damage,
        BonusValue.PISTOL_DAMAGE: commando_damage,
        BonusValue.SHOTGUN_DAMAGE: commando_damage,
        BonusValue.SR_DAMAGE: commando_damage
    }

    bonus_table = combine_bonus_tables(TalentSoldier.bonus_table, spec_table)


class TalentSoldierShockTrooper(TalentSoldier, Specialization):

    shock_trooper_dr: Lookup = {7: 0.06, 8: 0.08, 9: 0.10, 10: 0.12, 11: 0.14, 12: 0.16}

    spec_table = {
        BonusValue.HEALTH:   {7: 0.18, 8: 0.20, 9: 0.22, 10: 0.24, 11: 0.26, 12: 0.28},
        BonusValue.LIGHT_DR: shock_trooper_dr,
        BonusValue.MED_DR: shock_trooper_dr,
        BonusValue.HEAVY_DR: shock_trooper_dr,
    }

    bonus_table = combine_bonus_tables(TalentSoldier.bonus_table, spec_table)
