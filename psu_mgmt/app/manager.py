import builtins
import os

import yaml

from psu_mgmt.commands._maps import map_commands
from psu_mgmt.plugins._maps import map_plugins

MODEL_PATH = "models/"

default_config = {
    "model_name": "Example",
    "commands": [ # "name, [code], [page], [enabled]"
        {"name": "PMBus_00h_PAGE"},
        {"name": "PMBus_01h_OPERATION"},
        {"name": "PMBus_20h_VOUT_MODE"},
        {"name": "PMBus_3Ah_FAN_CONFIG_1_2"},
        {"name": "PMBus_3Bh_FAN_COMMAND_1"},
        {"name": "PMBus_79h_STATUS_WORD"},
        {"name": "PMBus_7Ah_STATUS_VOUT"},
        {"name": "PMBus_7Bh_STATUS_IOUT"},
        {"name": "PMBus_7Ch_STATUS_INPUT"},
        {"name": "PMBus_7Dh_STATUS_TEMPERATURE"},
        {"name": "PMBus_7Eh_STATUS_CML"},
        {"name": "PMBus_7Fh_STATUS_OTHER"},
        {"name": "PMBus_80h_STATUS_MFR_SPECIFIC"},
        {"name": "PMBus_81h_STATUS_FANS_1_2"},
        {"name": "PMBus_88h_READ_VIN"},
        {"name": "PMBus_89h_READ_IIN"},
        {"name": "PMBus_8Bh_READ_VOUT"},
        {"name": "PMBus_8Ch_READ_IOUT"},
        {"name": "PMBus_8Dh_READ_TEMPERATURE_1"},
        {"name": "PMBus_8Eh_READ_TEMPERATURE_2"},
        {"name": "PMBus_8Fh_READ_TEMPERATURE_3"},
        {"name": "PMBus_90h_READ_FAN_SPEED_1"},
        {"name": "PMBus_91h_READ_FAN_SPEED_2"},
        {"name": "PMBus_96h_READ_POUT"},
        {"name": "PMBus_97h_READ_PIN"},
    ],
    "plugins": [
        {"name": "ICSP_ST"},
        {"name": "ISP_CRPS"},
    ],
}

class ConfigurationManager:
    def __init__(self):
        self.setting = {}

        builtins.map_commands = map_commands # "ClassName": ClassName
        self.map_commands = [] # obj: ClassName

        builtins.map_plugins = map_plugins # "ClassName": ClassName
        self.map_plugins = [] # obj: ClassName

        file_path = ""
        if os.listdir(MODEL_PATH):
            file_paths = [file_path for file_path in os.listdir(MODEL_PATH) if file_path.endswith(".yaml")]
            if file_paths:
                file_path = os.path.join(MODEL_PATH, file_paths[0])

        self.init(file_path)

    def init(self, file_path):
        setting = self.load(file_path)
        self.map_commands = self.init_commands(setting)
        self.map_plugins = self.init_plugins(setting)

    def load(self, file_path: str):
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                setting = yaml.safe_load(f)
        else:
            setting = default_config
        return setting

    def init_commands(self, setting: dict):
        objs = []
        for entry in setting["commands"]:
            name = entry["name"]
            if name in builtins.map_commands:
                kwargs = {k: v for k, v in entry.items() if k != "name"}
                obj = builtins.map_commands[name](**kwargs)
                objs.append(obj)
        return objs

    def init_plugins(self, setting: dict):
        objs = []
        for entry in setting["plugins"]:
            name = entry["name"]
            if name in builtins.map_plugins:
                kwargs = {k: v for k, v in entry.items() if k != "name"}
                obj = builtins.map_plugins[name](**kwargs)
                objs.append(obj)
        return objs

class DatabaseManager:
    def __init__(self):
        pass

CONF = ConfigurationManager()
RMDB = DatabaseManager()
