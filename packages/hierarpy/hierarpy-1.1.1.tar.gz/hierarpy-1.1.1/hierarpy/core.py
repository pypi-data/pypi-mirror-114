import sys
import os
import yaml
from addict import Dict

def get_args():
    """Get any arguments provided by the user in the command line."""
    args = [arg[2:].split('=') for arg in sys.argv[1:]]
    return args

def load_config(cfg_path):
    """Load a nested configuration."""

    with open(cfg_path) as file:
        config = Dict(yaml.load(file, Loader=yaml.FullLoader))

    # now go through each subconfig and add it into our main config
    cfg_folder = os.path.split(cfg_path)[0]
    for subconfig_dict in config.subconfigs:
        folder, subconfig_name = [i for i in subconfig_dict.items()][0]
        subfolder = os.path.join(cfg_folder, folder)

        # we do this to handle any variant of the yaml file extension
        match = [f for f in os.listdir(subfolder) if subconfig_name == os.path.splitext(f)[0]][0]
        subconfig_path = os.path.join(subfolder, match)

        with open(subconfig_path) as file:
            subconfig = Dict(yaml.load(file, Loader=yaml.FullLoader))

        # add the identifier to the subconfig
        subconfig.subconfig_name = subconfig_name

        config[folder] = subconfig

    del config.subconfigs

    return config

def override_config(config, args):
    """Given some arguments represented as a list of tuples (key, value),
    replace such items in the config dict.
    """

    for key, value in args:
        # key will be something like model.autoregressive_type
        # value will be some kind of primitive type
        value = value.strip().replace('\'', '').replace('"','')

        if value in ['True', 'False', 'true', 'false']:
            value = True if value == 'True' else False
        elif value.isdigit():
            value = int(value)
        else:
            try:
                value = float(value)
            except ValueError:  # value is a string
                pass

        subconfig = config
        for keyval in key.split('.')[:-1]:
            subconfig = subconfig[keyval]
        subconfig[key.split('.')[-1]] = value

    return config
