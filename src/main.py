import yaml

from domain import Player, Enhancer


def load_data_from_yaml():
    with open("resources/stats.yaml", 'r') as fs:
        try:
            metadata = yaml.load(fs)
        except yaml.YAMLError as e:
            raise

        return metadata


def new_player(name):
    metadata = load_data_from_yaml()
    statistics = metadata['STATISTICS']

    player = Player(name)
    for statisticname in statistics:
        player.add_statistic(statisticname)

    base_enhancers = metadata['BASE_ENHANCERS']
    for base_enhancer in base_enhancers:
        enhancer_data = metadata['ENHANCERS'][base_enhancer]
        enhancer = Enhancer(enhancer_data['name'], enhancer_data['description'], enhancer_data['properties'])
        player.add_enhancer(enhancer)

    return player
