import yaml
from munch import munchify


def read_config(filename):
    """
    :type  filename: str
    :param filename: A YAML file containing the configuration
    :return: munch.Munch
    """
    with open(filename, 'r') as fp:
        try:
            docs = yaml.safe_load(fp)
            return munchify(docs)
        except yaml.YAMLError as e:
            print(e)
