import yaml

class ConfigReader:
        def __init__(self):
                pass

        def read_config(self, config_file):
                """
                        Reads a yaml file and returns the settings
                """
                with open(config_file,'r') as f:
                        config = yaml.safe_load(f)
                return config
