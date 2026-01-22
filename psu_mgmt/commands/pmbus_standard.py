from .pmbus import PMBus

class PMBus_00h_PAGE(PMBus):
    def __init__(self, **kwargs):
        super().__init__(self.__class__.__name__, **kwargs)
        self.rlen = 1

    def parse(self, raw):
        # parameter: [0, PEC]
        # return: "0", "Page 0"

        value = raw[0]
        text = f"Page {value}"

        return value, text

    def apply(self, value):
        # parameter: 0
        # return: 0x00, [0]

        return self.code, [value]

class PMBus_01h_OPERATION(PMBus):
    def __init__(self, **kwargs):
        super().__init__(self.__class__.__name__, **kwargs)
        self.rlen = 1

    def parse(self, raw):
        # parameter: [0x80, PEC]
        # return: "128", "ON, "

        value = raw[0]

        text = ""
        if value & 0x80 == 0x80:
            text += "ON, "
        else:
            text += "OFF, "

        if value & 0x20 == 0x20:
            text += "Margin High, "
        if value & 0x10 == 0x10:
            text += "Margin Low, "
        if value & 0x08 == 0x08:
            text += "Act On Fault, "
        if value & 0x04 == 0x04:
            text += "Ignore Fault, "

        return value, text

    def apply(self, value):
        # parameter: 0x80
        # return: 0x01, [0x80]

        return self.code, [value]
