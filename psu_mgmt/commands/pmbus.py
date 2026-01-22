import re

from .smbus import SMBus
from psu_mgmt.drivers.driver import Driver
from psu_mgmt.utils.crc import calc_crc8
from psu_mgmt.utils.misc import parse_code

class PMBus(SMBus):
    PEC = False # PMBus_19h
    VOUT_MODE = None # PMBus_20h

    def __init__(self, name="", code=None, rlen=0, page=None, enabled=True, **_):
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
        self.rlen = rlen

        if self.page is not None:
            self.name = f"{self.name} ({self.page})"

    def read(self, driver: Driver, device: str, address: int):
        cnt = 0
        if PMBus.PEC:
            cnt += 1

        if self.r_wbuf:
            w_raw = [address, self.code] + self.r_wbuf
            r_raw = driver.i2ctransfer(device, address, [self.code] + self.r_wbuf, self.rlen + cnt)
        elif self.page is None:
            w_raw = [address, self.code]
            r_raw = driver.i2ctransfer(device, address, [self.code], self.rlen + cnt)
        else:
            w_raw = [address, 0x06, 2, self.page, self.code]
            r_raw = driver.i2ctransfer(device, address, [0x06, 2, self.page, self.code], self.rlen + 2) # +CNT,PEC

        if not r_raw:
            return []

        if self.block:
            bcnt = r_raw[1]
            r_raw = r_raw[0:2+bcnt+cnt]

        raw = w_raw + r_raw

        if PMBus.PEC and calc_crc8(raw) != 0:
            return []

        if self.page is None:
            self.parse(r_raw[1:1+self.rlen])
        else:
            self.parse(r_raw[2:2+self.rlen])

        return raw

    def write(self, driver, device, address):
        raw = self.apply()

        if self.block:
            raw = [len(raw)] + raw

        if PMBus.PEC:
            raw.append(calc_crc8([address, self.code] + raw))

        return driver.i2ctransfer(device, address, [self.code] + raw, 0)

    def parse(self, raw):
        return 0, ""

    def apply(self, value):
        return []

    @staticmethod
    def linear16_parse(value):
        if PMBus.VOUT_MODE:
            value = value * PMBus.VOUT_MODE
            return value, f"{value:.2f} (V)"
        return 0, "No VOUT_MODE"

    @staticmethod
    def linear11_parse(value):
        exponent = (value >> 11) & 0x1F
        if exponent & 0x10:
            exponent -= 0x20
        mantissa = value & 0x07FF
        if mantissa & 0x400:
            mantissa -= 0x800
        return mantissa * (2 ** exponent)

    @staticmethod
    def linear11_encode(value):
        if value == 0:
            return 0x0000

        exponent = 0
        mantissa = round(value / (2 ** exponent))

        if mantissa < -1024 or mantissa > 1023:
            while mantissa < -1024 or mantissa > 1023:
                if exponent + 1 > 15:
                    break
                exponent += 1
                mantissa = round(value / (2 ** exponent))
        else:
            for e in range(exponent, -16, -1):
                m = round(value / (2 ** e))
                if m < -1024 or m > 1023:
                    break

                exponent = e
                mantissa = m

                v = m * (2 ** e)
                error = abs(value - v)
                if error == 0:
                    break

        if exponent < 0:
            exponent = 32 + exponent

        return (exponent << 11) + mantissa
