import pytest

from domain import Empire, Keywords


class TestPlayer:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.empire = Empire('Jimmy')

    def test_when_increasing_a_bonus_it_gets_computed(self):
        self.empire.add_bonus(bonus_name='Draw_card_on_settle', value=2)
        assert self.empire.get_bonus_value(bonus_name='Draw_card_on_settle') == 2

    def test_bonuses_should_increase_if_they_exist(self):
        self.empire.add_bonus(bonus_name='Draw_card_on_settle', value=2)
        self.empire.add_bonus(bonus_name='Draw_card_on_settle', value=3)
        assert self.empire.get_bonus_value(bonus_name='Draw_card_on_settle') == 5

    def test_increase_a_specific_world_bonus(self):
        self.empire.add_bonus(bonus_name='Military', value=3)
        assert self.empire.get_bonus_value(bonus_name='Military') == 3

    def test_return_0_if_no_bonus_has_been_added(self):
        assert self.empire.get_bonus_value(bonus_name='Draw_card_on_settle') == 0

    def test_nested_bonuses_stack(self):
        self.empire.add_bonus(bonus_name='Military', value=3)
        self.empire.add_bonus(bonus_name='Military_vs_Novelty', value=2)
        assert self.empire.get_bonus_value(bonus_name='Military') == 3
        assert self.empire.get_bonus_value(bonus_name='Military_vs_Novelty') == 5

    def test_add_planet_types_to_the_empire(self):
        self.empire.add_keyword(type=Keywords.GENES, amount=1)
        assert self.empire.get_keyword_count(type=Keywords.GENES) == 1

    def test_no_planet_of_type(self):
        assert self.empire.get_keyword_count(type=Keywords.MILITARY) == 0

    def test_add_military_per_imperium_bonus(self):
        self.empire.add_bonus(bonus_name='Military_per_imperium', value=1)
        self.empire.add_keyword(Keywords.IMPERIUM, 3)
        assert self.empire.get_bonus_value('Military_per_imperium') == 3
        self.empire.add_bonus(bonus_name='Military', value=2)
        assert self.empire.get_bonus_value('Military') == 5
