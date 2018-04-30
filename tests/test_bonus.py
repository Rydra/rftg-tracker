from domain import Bonus, Empire, Keywords


class TestBonus:
    def test_a_non_dependant_bonus(self):
        military_bonus = Bonus('Military', value=5)
        assert military_bonus.get_total_bonus() == 5

    def test_a_cummulative_bonus(self):
        military_bonus = Bonus('Military', value=5)
        military_vs_alien = Bonus('Military_vs_alien', value=2, enhanced_by=[military_bonus])
        assert military_vs_alien.get_total_bonus() == 7

    def test_some_bonuses_enhance_others(self):
        military_per_rebel = Bonus('Military_per_rebel', value=1, modifier=lambda v: v * 3)
        assert military_per_rebel.get_total_bonus() == 3

    def test_military_is_a_composed_bonus(self):
        player = Empire('Irene')
        player.add_cardkeyword(Keywords.REBEL, amount=3)

        military_per_rebel_world = Bonus('Military_per_Rebel_world', value=1, modifier=lambda v: v * player.get_cardkeywords(Keywords.REBEL))
        military_bonus = Bonus('Military', enhanced_by=[military_per_rebel_world], value=3)

        assert military_bonus.get_total_bonus() == 6

        player.add_cardkeyword(Keywords.REBEL, amount=1)

        assert military_bonus.get_total_bonus() == 7

    def test_military_as_non_military(self):
        military_as_non_military = Bonus('Military_as_non_military')
        settle_discounts = Bonus('Settle_discount', value=3)
        discount_when_using_military = Bonus('Discount_when_using_military', value=1, enhanced_by=[settle_discounts])
        assert discount_when_using_military.get_total_bonus() == 4

    def test_produce_on_windfall(self):
        produce_on_windfall = Bonus('Produce_on_any_windfall', value=2)
        produce_on_novelty_windfall = Bonus('Produce_on_novelty_windfall', value=3)