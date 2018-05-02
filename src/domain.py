from enum import Enum
from collections import Counter


class Bonus:
    """A Bonus whose value is its value plus others"""
    def __init__(self, name, enhanced_by=(), modifier=None, **kwargs):
        self.name = name
        self.enhanced_by = list(enhanced_by)
        self.modifier = modifier or (lambda p: p)
        self.value = kwargs.get('value', 0)

    def add_enhancer(self, enhance):
        self.enhanced_by.append(enhance)

    def get_total_bonus(self):
        return sum([enhancer.get_total_bonus() for enhancer in self.enhanced_by]) + self.modifier(self.value)

import yaml

with open("resources/bonus.yaml", 'r') as fs:
    try:
        bonus_metadata = yaml.load(fs)
    except yaml.YAMLError as e:
        raise

class Empire:
    NO_BONUS = Bonus('No bonus')
    def __init__(self, name, id=None, **kwargs):
        self.name = name
        self.bonuses = {}
        self.keywords = Counter()

    def get_bonus_value(self, bonus_name):
        return self.bonuses.get(bonus_name, self.NO_BONUS).get_total_bonus()

    def add_keyword(self, type, amount):
        self.keywords[type] += amount

    def add_bonus(self, bonus_name, value=1):
        """A factory method that takes the bonus metadata, creates the bonus and links
        it with other bonuses if necessary"""

        if bonus_name not in bonus_metadata:
            raise Exception(f'Unrecognized bonus {bonus_name}')

        metadata = bonus_metadata[bonus_name]
        bonus = self._create_bonus(bonus_name, metadata, value)
        self._enhance_other_bonuses(bonus, metadata)

        self.bonuses[bonus_name] = bonus

    def _enhance_other_bonuses(self, bonus, metadata):
        if 'enhances' in metadata:
            enhanced_bonuses = metadata['enhances']
            for enhanced_bonus in enhanced_bonuses:
                if enhanced_bonus not in self.bonuses:
                    self.bonuses[enhanced_bonus] = Bonus(name=enhanced_bonus, value=0)

                self.bonuses[enhanced_bonus].add_enhancer(bonus)

    def _create_bonus(self, bonus_name, metadata, value):
        modifier = self._get_modifier(metadata)

        value = value or metadata['value']
        if bonus_name in self.bonuses:
            # If the bonus is already assigned to the empire, just
            # retrieve it and increase its value
            bonus = self.bonuses[bonus_name]
            bonus.value += value
        else:
            bonus = Bonus(name=bonus_name, value=value, modifier=modifier)
        return bonus

    def _get_modifier(self, metadata):
        modifier = lambda v: v
        if 'multiplied_by' in metadata:
            type = Keywords[metadata['multiplied_by']]
            modifier = lambda v: v * self.keywords[type]
        return modifier

    def get_keyword_count(self, type):
        return self.keywords[type]


class Keywords(Enum):
    NOVELTY = 7
    RARE = 1
    GENES = 2
    ALIEN = 3
    NORMAL = 4
    REBEL = 5
    XENO = 8
    MILITARY = 9
    IMPERIUM = 10
    UPLIFT = 6
    DEVELOPMENT = 11
    ANTIXENO = 12


# Here we could define some metadata information
Military = Bonus('Military')
military_vs_novelty = Bonus('Military_vs_novelty', enhanced_by=[Military])
military_per_imperium = Bonus('Military_per_imperium')

#
# class SettleBonus:
#     DRAW_CARD_ON_PLACEMENT = 1
#     PLACE_MILITARY_AS_NON_MILITARY = 7
#     MILITARY = 6
#     DRAW_CARD = 2
#     APPLIES_ONLY_TO = 8
#     DISCOUNT = 3
#     XENO_DEFENSE = 4
#
#
# class BonusType(Enum):
#     TECHNOLOGY_DISCOUNT = 1
#
# class BonusCategory(Enum):
#     EXPLORE = 1
#     DEVELOP = 2
#     SETTLE = 3
#     TRADE = 4
#     CONSUME = 5
#     PRODUCE = 5
#
# class ExploreBonus(Enum):
#     SEE_EXTRA_CARDS = 1
#     GRAB_EXTRA_CARDS = 2
#     EXTRA_CARDS_PER_REBEL_PLANET = 3
#
# class DevelopBonus(Enum):
#     DRAW_CARD_ON_PLACEMENT = 1
#     DRAW_CARD = 2
#     DISCOUNT = 3
#
# class WorldType(Enum):
#     ALL = 6
#     NOVELTY = 7
#     RARE = 1
#     GENES = 2
#     ALIEN = 3
#     NORMAL = 4
#     REBEL = 5
#     XENO = 8
#     MILITARY = 9
#
# class TradeBonus(Enum):
#     DRAW_EXTRA_CARDS = 1
#
#
# class ProduceBonus(Enum):
#     DRAW_CARD = 1
#     REPAIR = 2
#     PRODUCE_WINDFALL = 3
#     DRAW_CARD_PER_PLANET = 4
#
# bonus_set = {
#     BonusCategory.EXPLORE: {
#         ExploreBonus.SEE_EXTRA_CARDS: 0,
#         ExploreBonus.GRAB_EXTRA_CARDS: 0,
#         ExploreBonus.EXTRA_CARDS_PER_REBEL_PLANET: False
#     },
#     BonusCategory.DEVELOP: {
#         DevelopBonus.DRAW_CARD: 0,
#         DevelopBonus.DRAW_CARD_ON_PLACEMENT: 0,
#         DevelopBonus.DISCOUNT: 0
#     },
#     BonusCategory.SETTLE: {
#         SettleBonus.DRAW_CARD_ON_PLACEMENT: 0,
#         SettleBonus.MILITARY: {
#             WorldType.NORMAL: 0,
#             WorldType.GENES: 0,
#             WorldType.NOVELTY: 0,
#             WorldType.RARE: 0,
#             WorldType.ALIEN: 0,
#             WorldType.REBEL: 0,
#             WorldType.XENO: 0
#         },
#         SettleBonus.DISCOUNT: {
#             WorldType.NORMAL: 0,
#             WorldType.GENES: 0,
#             WorldType.NOVELTY: 0,
#             WorldType.RARE: 0,
#             WorldType.ALIEN: 0
#         },
#         SettleBonus.PLACE_MILITARY_AS_NON_MILITARY: {
#             'Available': False,
#             SettleBonus.APPLIES_ONLY_TO: WorldType.ALL,
#             SettleBonus.DISCOUNT: 0
#         },
#         SettleBonus.XENO_DEFENSE: 0
#
#     },
#     BonusCategory.TRADE: {
#         TradeBonus.DRAW_EXTRA_CARDS: {
#             WorldType.ALL: 0,
#             WorldType.GENES: 0,
#             WorldType.NOVELTY: 0,
#             WorldType.RARE: 0,
#             WorldType.ALIEN: 0,
#             WorldType.REBEL: 0
#         }
#     },
#     BonusCategory.CONSUME: {
#
#     },
#     BonusCategory.PRODUCE: {
#         ProduceBonus.DRAW_CARD: 0,
#         ProduceBonus.REPAIR: 0,
#         ProduceBonus.PRODUCE_WINDFALL: {
#             WorldType.ALL: 0,
#             WorldType.GENES: 0,
#             WorldType.NOVELTY: 0,
#             WorldType.RARE: 0,
#             WorldType.ALIEN: 0,
#         },
#         ProduceBonus.DRAW_CARD_PER_PLANET: {
#             WorldType.XENO: 0,
#             WorldType.MILITARY: 1
#         }
#     }
# }