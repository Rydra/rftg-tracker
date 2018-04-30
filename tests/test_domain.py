import pytest

from domain import Empire, Keywords, Bonus


class TestPlayer:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.player = Empire('Jimmy')

    def test_when_increasing_a_bonus_it_gets_computed(self):
        draw_card_on_settle_bonus = Bonus('Draw_card_on_settle', value=2)
        self.player.add_bonus(bonus=draw_card_on_settle_bonus)
        assert self.player.get_bonus_value(bonus_name='Draw_card_on_settle') == 2

    def test_bonuses_should_increase_if_they_exist(self):
        draw_card_on_settle_bonus = Bonus('Draw_card_on_settle', value=2)
        draw_card_on_settle_bonus_2 = Bonus('Draw_card_on_settle', value=3)
        self.player.add_bonus(bonus=draw_card_on_settle_bonus)
        self.player.add_bonus(bonus=draw_card_on_settle_bonus_2)
        assert self.player.get_bonus_value(bonus_name='Draw_card_on_settle') == 5

    def test_increase_a_specific_world_bonus(self):
        self.player.add_bonus(bonus=Bonus('Military', value=3))
        assert self.player.get_bonus_value(bonus_name='Military') == 3

    def test_return_0_if_no_bonus_has_been_added(self):
        assert self.player.get_bonus_value(bonus_name='Draw_card_on_settle') == 0

    def test_nested_bonuses_stack(self):
        self.player.add_bonus2(bonus_name='Military', value=3)
        self.player.add_bonus2(bonus_name='Military_vs_Novelty')
        assert self.player.get_bonus_value(bonus_name='Military') == 3
        assert self.player.get_bonus_value(bonus_name='Military_vs_Novelty') == 5

    def test_add_planet_types_to_the_empire(self):
        self.player.add_cardkeyword(type=Keywords.GENES, amount=1)
        assert self.player.get_cardkeywords(type=Keywords.GENES) == 1

    def test_no_planet_of_type(self):
        assert self.player.get_cardkeywords(type=Keywords.MILITARY) == 0

    def test_add_military_per_imperium_bonus(self):
        self.player.add_bonus2(bonus_name='Military_per_imperium', value=1)
        self.player.add_cardkeyword(Keywords.IMPERIUM, 3)
        assert self.player.get_bonus_value('Military_per_imperium') == 3
        self.player.add_bonus2(bonus_name='Military', value=2)
        assert self.player.get_bonus_value('Military') == 5
