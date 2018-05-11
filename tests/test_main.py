from domain import Enhancer
from main import new_player


def test_initializing_a_new_player():
    player = new_player('paco')
    statistics = player.get_statistics()
    assert statistics['MILITARY'].actual_value == 0
    assert statistics['MILITARY VS NOVELTY'].actual_value == 0

    enhacer = Enhancer('Some enhancer', None, properties=[{'statistic': 'MILITARY', 'value': 3, 'factor': 'additive'}])
    player.add_enhancer(enhacer)
    statistics = player.get_statistics()
    assert statistics['MILITARY'].actual_value == 3
    assert statistics['MILITARY VS NOVELTY'].actual_value == 3 # It doesn't work because of the base value!
