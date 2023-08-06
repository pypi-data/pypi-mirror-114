import yaml
from platformer.defaults import base_config

class PlatformerConfigReader():
    def __init__(self, yaml_text, default="base_config"):
        self.config_yaml = yaml.safe_load(yaml_text)
        self.config =  self.input_defaults(self.config_yaml)

    def input_defaults(self, config):
        config_merged = config
        print("Fill default values")
        return config_merged





