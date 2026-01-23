import builtins
from datetime import datetime
import importlib.util
import os
import sqlite3
import sys

import yaml

from psu_mgmt.commands._maps import map_commands
from psu_mgmt.plugins._maps import map_plugins

MODEL_PATH = "models/"
RMDB_PATH = "log.db"

default_model = {
    "model_name": "default",
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

def load_module(module_name, module_path):
    if module_name in sys.modules:
        return

    if not os.path.exists(module_path):
        return

    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    sys.modules[module_name] = module

class ConfigurationManager:
    def __init__(self):
        builtins.map_commands = map_commands
        builtins.map_plugins = map_plugins

        self.model_name = ""
        self.list_commands = []
        self.list_plugins = []

        file_path = ""
        if os.listdir(MODEL_PATH):
            file_paths = [file_path for file_path in os.listdir(MODEL_PATH) if file_path.endswith(".yaml")]
            if file_paths:
                file_path = os.path.join(MODEL_PATH, file_paths[0])

        self.init(file_path)

    def init(self, file_path):
        self.load_module(file_path)

        setting = self.load_config(file_path)
        self.model_name = setting["model_name"]
        self.list_commands = self.init_commands(setting)
        self.map_plugins = self.init_plugins(setting)

    # private api

    def load_module(self, file_path):
        module_name = os.path.splitext(os.path.basename(file_path))[0]
        module_path = os.path.splitext(file_path)[0] + '.py'
        load_module(module_name, module_path)

    def load_config(self, file_path: str):
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                setting = yaml.safe_load(f)
        else:
            setting = default_model
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
        self.conn = sqlite3.connect(RMDB_PATH)
        self.curr = self.conn.cursor()

        self.create_log_table("temp")
        self.curr.execute("DELETE FROM temp;")
        self.conn.commit()
        self.curr.execute("VACUUM;")

        self.table_ptr = ""

    def start(self):
        datetime_str = datetime.now().strftime("%y%m%d_%H%M%S") # 20260120_140635

        self.create_log_table(datetime_str)

        self.table_ptr = datetime_str

    def insert(self, table, name, value, result, raw):
        datetime_str = datetime.now().strftime("%y%m%d_%H%M%S") # 20260120_140635

        self.curr.execute(f"""
            INSERT INTO {table} VALUES (?, ?, ?, ?, ?);
        """, datetime_str, name, value, result, raw)

        self.conn.commit()

    def create_log_table(self, table_name):
        self.curr.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                datetime    TEXT,
                name        TEXT,
                value       TEXT,
                result      TEXT,
                raw         TEXT
            );
        """)

CONF = ConfigurationManager()
RMDB = DatabaseManager()
