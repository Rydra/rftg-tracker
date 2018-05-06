import operator
from collections import Counter, defaultdict

import yaml

with open("resources/bonus.yaml", 'r') as fs:
    try:
        bonus_metadata = yaml.load(fs)
    except yaml.YAMLError as e:
        raise


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
    def __init__(self, name, value=0):
        self.name = name
        self.value = value

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

    def add_statistic(self, statistic_name, value=0):
        self.statistics[statistic_name] = Statistic(statistic_name, value)

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
        for statname, properties in properties_by_stat.items():
            actual_statistics[statname] = self._compute_actual_statistic(statname, properties)

        return actual_statistics

    def _compute_actual_statistic(self, statname, properties):
        statistic = self.statistics[statname]
        current_value = statistic.value
        for property in properties:
            factor = operator.mul if property['factor'] == 'multiplicative' else operator.add

            dependant_keyword_factor = 1 if 'depends_on_keyword' not in property else self.get_keyword_count(
                property['depends_on_keyword'])
            value_to_multiply = dependant_keyword_factor * property['value']
            current_value = factor(current_value, value_to_multiply)

        return ActualStatistic(statname, statistic.value, current_value)

    def _group_properties_by_statistic(self):
        properties_dict = defaultdict(list)
        for enhancer in self.enhancers:
            for statname, properties in enhancer.properties.items():
                properties_dict[statname] += properties

        return properties_dict

    def increase_statistic(self, statistic_name, value):
        self.statistics[statistic_name].increase_base_value(value)

    def add_keyword(self, type, amount):
        self.keywords[type] += amount

    def get_keyword_count(self, type):
        return self.keywords[type]
