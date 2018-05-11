from collections import Counter, defaultdict
from functools import reduce

from formula import Formula


# We could also call them StatModifier
class Enhancer:
    def __init__(self, name, description, properties):
        self.name = name
        self.description = description
        self.properties = defaultdict(list)

        for property in properties:
            self.properties[property['statistic']].append(property)

    def apply(self, player):
        pass


class Statistic:
    def __init__(self, name, value=0, description=None, needs_rounding=True):
        self.name = name
        self.value = value
        self.description = description
        self.needs_rounding = needs_rounding

    def increase_base_value(self, amount):
        self.value += amount

    def get_value(self):
        return self.value


class ActualStatistic:
    def __init__(self, statistic_name, original_value, actual_value):
        self.statistic_name = statistic_name
        self.original_value = original_value
        self.actual_value = actual_value


class Player:
    def __init__(self, name):
        self.name = name
        self.keywords = Counter()

        self.enhancers = []
        self.statistics = {}

    def add_enhancer(self, enhancer):
        self.enhancers.append(enhancer)

    def add_statistic(self, statistic_name, value=0, **kwargs):
        self.statistics[statistic_name] = Statistic(statistic_name, value, **kwargs)
        self.keywords[statistic_name] += value

    def get_statistics(self):
        # NOTES: Why compute how do the different enhancers alter the statistics here instead of passing
        # by the player or statistics to the enhancer and let it alter the statistic on its own way?
        # The answer: Some enhancer may alter several stats, either multiplicatively or additively.
        # Since the order of the factors can alter the result depending on the order they are applied,
        # If we first gather all the properties together we may sort them and have greater control on how they are applied.
        # The enhancer by itself could not control the order he should be processed (but a player or a service who
        # has context could!)
        properties_by_stat = self._group_properties_by_statistic()

        actual_statistics = {}
        for statistic in self.statistics.values():
            actual_statistics[statistic.name] = self._compute_actual_statistic(statistic.name, properties_by_stat.get(statistic.name, []))

        return actual_statistics

    def _compute_property_value(self, property):
        value = property['value']
        if 'depends_on' in property:
            value = value * self.get_keyword_count(property['depends_on'])

        return value

    def _compute_actual_statistic(self, statname, properties):
        statistic = self.statistics[statname]
        current_value = statistic.value

        multiplicators = sum(self._compute_property_value(property) for property in properties if property['factor'] == 'multiplicative')
        additions = sum(self._compute_property_value(property) for property in properties if property['factor'] == 'additive')
        formulas = [Formula(property['formula']) for property in properties if property['factor'] == 'custom']

        # Usually used for percentages that should not ever reach 100%
        additive_multiplicatively = [self._compute_property_value(property) for property in properties if property['factor'] == 'additive-multiplicatively']

        if additive_multiplicatively:
            additive_multiplicatively_value = reduce(lambda x, y: x + x * y, sorted(additive_multiplicatively))
        else:
            additive_multiplicatively_value = 0

        if not formulas:
            current_value = statistic.value * max(1, multiplicators) + additions + additive_multiplicatively_value

        else:
            formula_keywords = {'MULTIPLICATORS', 'ADDITIONS', 'ADDITIVE_MULTIPLICATIVELY', 'base_value'}
            for formula in formulas:
                variables = set(formula.variables) - formula_keywords
                locals = dict((variable, self.get_keyword_count(variable)) for variable in variables)
                locals.update({
                    'base_value': statistic.value,
                    'ADDITIONS': additions,
                    'MULTIPLICATORS': max(1, multiplicators),
                    'ADDITIVE_MULTIPLICATIVELY': additive_multiplicatively_value
                })
                current_value = formula.evaluate(locals)

        return ActualStatistic(statname, statistic.value, round(current_value) if statistic.needs_rounding else current_value)

    def _group_properties_by_statistic(self):
        properties_dict = defaultdict(list)
        for enhancer in self.enhancers:
            for statname, properties in enhancer.properties.items():
                properties_dict[statname] += properties

        return properties_dict

    def increase_statistic(self, statistic_name, value):
        self.statistics[statistic_name].increase_base_value(value)
        self.keywords[statistic_name] += value

    def add_keyword(self, type, amount):
        self.keywords[type] += amount

    def get_keyword_count(self, type):
        return self.keywords[type]
