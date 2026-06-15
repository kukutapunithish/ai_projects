import yaml

with open('config/model_config.yaml', 'r') as file:
    MODEL_CONFIG = yaml.safe_load(file)

with open('config/retrieval_config.yaml', 'r') as file:
    RETRIEVAL_CONFIG = yaml.safe_load(file)