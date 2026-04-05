import yaml

with open('config/model_config.yaml', 'r') as file:
    CONFIG = yaml.safe_load(file)