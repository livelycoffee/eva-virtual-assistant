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
        self.config: dict[str, Any] | None = None
        self.load_config_file()

    def load_config_file(self) -> None:
        try:
            with open(self.CONFIG_FILE, "r") as cf:
                self.config = yaml.safe_load(cf) or {}
        except FileNotFoundError:
            raise ConfigException(f"Config file '{self.CONFIG_FILE}' not found")

    def get_parameter(self, param: str, required: bool = False) -> Any: # --> Use only if parameter is REQUIRED (Strict)
        if self.config is None:
            raise ConfigException("Config file not loaded")
        
        params = param.split(".")
        result = self.config

        for _param in params:
            if _param not in result:
                raise ConfigException(f"Missing config parameter: '{_param}'")
            result = result[_param]
        if result is None and required:
            raise ConfigException(f"No value defined for parameter: '{param}'")
        return result
           
    def get(self, param: str, default: Any = None, required: bool = False) -> Any: # --> General use cases (use default)
        if self.config is None:
            raise ConfigException("Config file not loaded")
        
        if default is None and required:
            raise ConfigException("No value set for 'default' but is required")
        
        params = param.split(".")
        result = self.config

        for _param in params:
            if _param not in result:
                return default
            result = result.get(_param, default)
        if result is None and required:
            return default
        return result

    def set_parameter(self, param: str, value: Any, required: bool = False) -> None:
        if self.config is None:
            raise ConfigException("Config file not loaded")
        if value is None and required:
            raise ConfigException(f"No value provided for '{param}' but is required")
        self.config[param] = value

    def update_config_file(self) -> None:
        try:
            with open(self.CONFIG_FILE, "w") as cf:
                yaml.safe_dump(data=self.config, stream=cf, sort_keys=False)
        except FileNotFoundError:
            raise ConfigException(f"Config file '{self.CONFIG_FILE}' not found")

#*---------- END OF CODE ----------*