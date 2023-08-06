import yaml

class PlatformerConfigReader():
    def __init__(self, yaml_text):
        self.config_yaml = yaml.safe_load(yaml_text)
        self.config =  self._input_defaults(self.config_yaml)

    def _find_definition(self, name):
        not_found = f"Definition {name} not found on config file"
        if result := self.config.get(name, None):
            return result
        else:
            return not_found
            exit(-1)


    def _input_defaults(self, config):
        config_merged = config
        print("Fill default values")
        return config_merged

    def get_terraform(self, ):
        return self._find_definition("terraform")






