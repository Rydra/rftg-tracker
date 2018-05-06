from domain import Statistic, Enhancer, Player


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
        'depends_on_keyword': 'POCKET'
    }]

    pocket_master = Enhancer(name='Pocket master', description=description, properties=properties)

    player = Player('Hercule')
    player.add_statistic('MIGHT', value=2)
    player.add_keyword('POCKET', amount=4)
    player.add_enhancer(pocket_master)

    statistics = player.get_statistics()
    assert statistics['MIGHT'].actual_value == 7
