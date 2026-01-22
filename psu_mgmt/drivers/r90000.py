import logging
import time

from pywinusb import hid

from .driver import Driver

logger = logging.getLogger(__name__)

class R90000(Driver):
    def __str__(self):
        if not self.device:
            return "NULL"
        return str(self.device_path)

    def __init__(self):
        self.device = None
        self.device_path = ""

        self.i2c_report = None
        self.conf_report = None
        self.buf = []

        self.reconnect()

    # Public API

    @staticmethod
    def search_devices():
        devices = []

        # R90000-9271
        devices += hid.HidDeviceFilter(vendor_id=0x04D8, product_id=0x003F).get_devices()

        # R90000-9150
        devices += hid.HidDeviceFilter(vendor_id=0x04D8, product_id=0x0040).get_devices()

        return devices

    def reconnect(self):
        if self.device:
            if self.device.is_opened():
                self.device.close()

        devices = R90000.search_devices()
        if self.set_device_by_path(self.device_path):
            return

        if len(devices) == 1:
            self.device_init(devices[0])

    def set_device_by_path(self, device_path):
        devices = R90000.search_devices()
        for device in devices:
            if device.device_path == device_path:
                self.device_init(device)
                return True
        return False

    def conf(self, timeout):
        low_byte = timeout % 256
        high_byte = timeout // 256

        buf = [0x0F, 9, 0x41, 0x43, 0x00] + [0x00, 0x00, low_byte, high_byte] + [0x0D, 0x0A]
        buf += [0] * (64 - len(buf))

        try:
            self.conf_report.send(buf)
        except Exception as e:
            logger.error("%s", e)
            self.reconnect()
            return False

        return True

    def i2ctransfer(self, device, address, wbuf, rlen):
        # issue
        if len(wbuf) > 0 and wbuf[-1] == 0x0D:
            wbuf.append(0x0D)

        buf = [0x05, (10 + len(wbuf)), 0x41, 0x44, address] + wbuf + [0x0D, 0x0A, address+1, rlen, 0x0D, 0x0A]
        buf += [0] * (64 - len(buf))

        self.buf = [0x15, rlen + 6]
        try:
            self.i2c_report.send(buf)
        except Exception as e:
            logger.error("%s", e)
            self.reconnect()
            return []

        time.sleep(0.01)
        count = 0
        while self.buf[1] > len(self.buf) and count <= 4:
            time.sleep(0.025)
            count += 1
        buf = self.buf.copy()

        if rlen == 0:
            return []
        if len(buf) < 4:
            return []
        if buf[3] == 67: # 0x43, timeout
            return []

        buf = [address+1] + buf[6:6+rlen]
        return buf

    # Private API

    def device_init(self, device):
        self.device = device
        self.device_path = self.device.device_path

        if not self.device.is_opened():
            self.device.open()
        self.device.set_raw_data_handler(self.raw_data_handler)

        output_reports = self.device.find_output_reports()
        # for report in output_reports:
        #     logger.info("Report ID: %s", report.report_id)
        self.i2c_report = output_reports[4]
        self.conf_report = output_reports[10]

    def raw_data_handler(self, data):
        if data[0] != 0x15: # I2C callback
            return
        self.buf += list(data[2:])
