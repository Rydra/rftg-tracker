import parser
from functools import reduce

from domain import Statistic, Enhancer, Player
from formula import Formula


def test_a_statistic_has_a_name_and_a_base_value():
    statistic = Statistic('MILITARY', 5)
    assert statistic.get_value() == 5

def test_an_empire_can_add_enhancers():
    properties = [
        {
            'statistic': 'MILITARY',
            'value': 2,
            'factor': 'multiplicative'
        },
        {
            'statistic': 'DRAW_CARDS_ON_EXPLORE',
            'value': 0.5,
            'factor': 'multiplicative'
        }
    ]
    description = 'Boosts military, but halves the amount of cards you see when exploring'
    uberBombardier = Enhancer(name='UberBombardier', description=description, properties=properties)

    empire = Player('Cherrymilk')
    empire.add_enhancer(uberBombardier)
    empire.add_statistic('MILITARY', value=2)
    empire.add_statistic('DRAW_CARDS_ON_EXPLORE')

    statistics = empire.get_statistics()

    assert statistics['MILITARY'].original_value == 2
    assert statistics['MILITARY'].actual_value == 4
    assert statistics['DRAW_CARDS_ON_EXPLORE'].actual_value == 0

def test_compatible_with_any_kind_of_game():
    description = 'Increases you defense and stamina, but reduces your speed'
    properties = [
        {
            'statistic': 'DEFENSE',
            'value': +5,
            'factor': 'additive'
        },
        {
            'statistic': 'STAMINA',
            'value': +2,
            'factor': 'additive'
        },
        {
            'statistic': 'SPEED',
            'value': -2,
            'factor': 'additive'
        }
    ]
    hylian_shield = Enhancer(name='Hylian Shield', description=description, properties=properties)

    empire = Player('Cherrymilk')
    empire.add_statistic('DEFENSE', value=5)
    empire.add_statistic('STAMINA', value=4)
    empire.add_statistic('SPEED', value=4)

    empire.add_enhancer(hylian_shield)

    statistics = empire.get_statistics()

    assert statistics['DEFENSE'].actual_value == 10
    assert statistics['STAMINA'].actual_value == 6
    assert statistics['SPEED'].actual_value == 2

def test_some_bonuses_may_depend_on_player_caracteristics():
    description = 'Boosts your might by one plus the number of pockets you have'  # For real
    properties = [{
        'statistic': 'MIGHT',
        'value': 1,
        'factor': 'additive'
    },
    {
        'statistic': 'MIGHT',
        'value': 1,
        'factor': 'additive',
        'depends_on': 'POCKET'
    }]

    pocket_master = Enhancer(name='Pocket master', description=description, properties=properties)

    player = Player('Hercule')
    player.add_statistic('MIGHT', value=2)
    player.add_keyword('POCKET', amount=4)
    player.add_enhancer(pocket_master)

    statistics = player.get_statistics()
    assert statistics['MIGHT'].actual_value == 7

def test_stats_are_enhancers_as_well():
    description = 'Increases your ability to run, but for every 5 points you lose 1 point of strength'
    properties = [
        {
            'statistic': 'STRENGTH',
            'value': -1 / 5,
            'factor': 'additive',
            'depends_on': 'RUNNING'
        }
    ]

    stat_enhancer = Enhancer(name="Speed per Strength", description=description, properties=properties)

    player = Player('Hercule')
    player.add_statistic('RUNNING', value=7)
    player.add_statistic('STRENGTH', value=4)
    player.add_enhancer(stat_enhancer)

    statistics = player.get_statistics()
    assert statistics['STRENGTH'].actual_value == 3

def test_some_stats_require_multiplicative_percentages():
    description = 'Increases your chance to dodge'
    properties = [
        {
            'statistic': 'DODGE',
            'value': 0.25,
            'factor': 'additive-multiplicatively'
        }
    ]
    ninja_boots = Enhancer(name='Ninja Boots', description=description, properties=properties)

    player = Player('Tixus')
    player.add_statistic('DODGE', value=0, needs_rounding=False)
    player.add_enhancer(ninja_boots)
    player.add_enhancer(ninja_boots)

    statistics = player.get_statistics()
    assert statistics['DODGE'].actual_value == 0.3125

def test_enhancers_may_define_their_own_formula():
    # Custom enhancers are applied in the end of all calculations
    description = 'Increases magic due to some secret formula'
    properties = [
        {
            'statistic': 'MAGIC',
            'factor': 'custom',
            'formula': 'base_value * MULTIPLICATORS + STAMINA // 3 - SPEED // 5 + ADDITIONS'
        },
        {
            'statistic': 'MAGIC',
            'value': 2,
            'factor': 'multiplicative'
        },
        {
            'statistic': 'MAGIC',
            'value': 3,
            'factor': 'additive'
        }
    ]

    stat_enhancer = Enhancer(name="Wild magic", description=description, properties=properties)

    player = Player('Hercule')
    player.add_statistic('SPEED', value=7)
    player.add_statistic('MAGIC', value=2)
    player.add_enhancer(stat_enhancer)

    statistics = player.get_statistics()
    assert statistics['MAGIC'].actual_value == 6

def test_formula_expressions_can_be_parsed():
    formula = parser.expr('base_value * MULTIPLIER + STAMINA // 3 - SPEED // 5 + ENHANCERS').compile()
    value = eval(formula, {}, {'base_value': 3, 'MULTIPLIER': 1, 'STAMINA': 3, 'SPEED': 10, 'ENHANCERS': 3})
    assert value == 5

    # expr = NumExpr('base_value * MULTIPLIER + STAMINA / 3 - SPEED / 5 + ENHANCERS')

    variables = {'base_value': 3, 'MULTIPLIER': 1, 'STAMINA': 3, 'SPEED': 10, 'ENHANCERS': 3, 'BANANAS': 8}

    formula = Formula('base_value * MULTIPLIER + STAMINA // 3 - SPEED // 5 + ENHANCERS')
    assert formula.evaluate(variables) == 5

def test_reduce_with_multiplicative_formulas():
    assert reduce(lambda x, y: x + x * y, [0.5, 0.5, 0.25]) == 0.9375
