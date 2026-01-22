import re

from .smbus import SMBus
from psu_mgmt.driver.driver import Driver
from psu_mgmt.utils.crc import calc_crc8

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

    def read(self, driver: Driver, device: str, address: int):
        cnt = 0
        if PMBus.PEC:
            cnt += 1

        if self.r_wbuf:
            w_raw = [address, self.code] + self.r_wbuf
            r_raw = driver.i2ctransfer(device, w_raw, self.rlen + cnt)
        elif self.page is None:
            w_raw = [address, self.code]
            r_raw = driver.i2ctransfer(device, w_raw, self.rlen + cnt)
        else:
            w_raw = [address, 0x06, 2, self.page, self.code]
            r_raw = driver.i2ctransfer(device, w_raw, self.rlen + 2) # +CNT,PEC

        if not r_raw:
            return []

        if self.block:
            bcnt = r_raw[1]
            r_raw = r_raw[0:2+bcnt+cnt]

        raw = w_raw + r_raw

        if PMBus.PEC and calc_crc8(raw) != 0:
            return []

        if self.page is None:
            self.parse(r_raw[1:1+self.length])
        else:
            self.parse(r_raw[2:2+self.length])

        return raw

    def write(self, driver, device, address):
        raw = self.apply()

        if self.block:
            raw = [len(raw)] + raw

        if PMBus.PEC:
            raw.append(calc_crc8([address, self.code] + raw))

        return driver.i2ctransfer(device, [address, self.code] + raw, 0)

    def parse(self, raw):
        raise NotImplementedError("parse function must be defined!")

    def apply(self, value):
        raise NotImplementedError("apply function must be defined!")

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
