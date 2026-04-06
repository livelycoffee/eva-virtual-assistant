# ---------- IMPORTS ----------

import yaml
from typing import Any

# ---------- CONFIG FILE ----------

CONFIG_FILE = "assets/system/config.yaml" # Hardcoded --> DO NOT CHANGE unless you know what you are doing

# ---------- CONFIG EXCEPTION CLASS ----------

class ConfigException(Exception):
    pass

# ---------- CONFIG CLASS DEFINITION ----------

class Config:
    def __init__(self):
        self.CONFIG_FILE = CONFIG_FILE
        global config

    def load_config_file(self) -> None:
        try:
            with open(self.CONFIG_FILE, "r") as cf:
                Config.config = yaml.safe_load(cf) or {}
        except FileNotFoundError:
            raise ConfigException(f"Config file '{self.CONFIG_FILE}' not found")

    def get_parameter(self, param: str) -> Any: # --> Use only if parameter is REQUIRED (Strict)
        if Config.config is None:
            raise ConfigException("Config file not loaded")
        
        params = param.split(".")
        result = Config.config

        for _param in params:
            if _param not in result:
                raise ConfigException(f"Missing config parameter: '{_param}'")
            result = result[_param]
        return result
           
    def get(self, param: str, default: Any = None) -> Any: # --> General use cases (use default)
        if Config.config is None:
            raise ConfigException("Config file not loaded")
        
        params = param.split(".")
        result = Config.config

        for _param in params:
            if _param not in result:
                return default
            result = result.get(_param, default)
        return result

    def set_parameter(self, param: str, value: Any) -> None:
        if Config.config is None:
            raise ConfigException("Config file not loaded")
        Config.config[param] = value

    def update_config_file(self) -> None:
        try:
            with open(self.CONFIG_FILE, "w") as cf:
                yaml.safe_dump(data=Config.config, stream=cf, sort_keys=False)
        except FileNotFoundError:
            raise ConfigException(f"Config file '{self.CONFIG_FILE}' not found")

#*---------- END OF CODE ----------*