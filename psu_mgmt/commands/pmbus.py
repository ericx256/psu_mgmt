import re

from .smbus import SMBus

class PMBus(SMBus):
    PEC = False # PMBus_19h
    VOUT_MODE = None # PMBus_20h

    def __init__(self, name="", code=None, page=None, enabled=True, **_):
        super().__init__()
        self.block = False
        self.page = page
        self.enabled = enabled

        if name: # PMBus_XXh_CmdName
            m = re.search(r'^([A-Za-z0-9]+)_([0-9A-Fa-f]+)h_(.+)$', name)
            if m:
                code = int(m.group(2), 16) # XXh
                name = m.group(3) # CmdName

        self.name = name
        self.code = parse_code(code)

        if self.page is not None:
            self.name = f"{self.name} ({self.page})"

def parse_code(code):
    if isinstance(code, int):
        value = code

    else:
        code_str = str(code).strip().lower()

        # "0x40"
        if code_str.startswith("0x"):
            value = int(code_str, 16)

        # "40h"
        elif code_str.endswith("h"):
            value = int(code_str[:-1], 16)

        # "64"
        elif code_str.isdigit():
            value = int(code_str)

        else:
            raise ValueError(f"Invalid code format: {code}")

    if not (0 <= value <= 255):
        raise ValueError(f"Code out of range (0~255): {value}")

    return value
