import os
import yaml
from munch import munchify

DIRNAME = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(DIRNAME, 'data', 'configs')

def read_config(filename):
    """
    :type  filename: str
    :param filename: A YAML file containing the configuration
    :return: munch.Munch
    """
    with open(filename, 'r') as fp:
        docs = yaml.safe_load(fp)
        return munchify(docs)
