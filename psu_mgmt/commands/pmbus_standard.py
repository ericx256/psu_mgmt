from .pmbus import PMBus

class PMBus_00h_PAGE(PMBus):
    def __init__(self, **kwargs):
        super().__init__(self.__class__.__name__, **kwargs)
        self.rlen = 1

    def analysis(self, value):
        return f"Page {value}"

    def parse(self, raw):
        value = raw[0]
        return value, self.analysis(value)

    def apply(self, value):
        return [value]

class PMBus_01h_OPERATION(PMBus):
    def __init__(self, **kwargs):
        super().__init__(self.__class__.__name__, rlen=1, **kwargs)

    def analysis(self, value):
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

        return text

    def parse(self, raw):
        value = raw[0]
        return value, self.analysis(value)

    def apply(self, value):
        return [value]

class PMBus_02h_ON_OFF_CONFIG(PMBus):
    def __init__(self, **kwargs):
        super().__init__(self.__class__.__name__, rlen=1, **kwargs)

    def analysis(self, value):
        text = ""
        if value & 0x10 == 0x10:
            text += "Power up by ["

            if value & 0x08 == 0x08:
                text += "01h, "

            if value & 0x04 == 0x04:
                text += "PSON"

            text += "]"
        else:
            text += "Power up any time ["

            if value & 0x08 == 0x08:
                text += "?, "

            if value & 0x04 == 0x04:
                text += "?"

            text += "]"

        text += "\n"

        if value & 0x02 == 0x02:
            text += "PSON active High, "
        else:
            text += "PSON active Low, "

        if value & 0x01 == 0x01:
            text += "Shutdown immediate"
        else:
            text += "Shutdown delay"

        return text

    def parse(self, raw):
        value = raw[0]
        return value, self.analysis(value)

    def apply(self, value):
        return [value]

class PMBus_19h_CAPABILITY(PMBus):
    def __init__(self, **kwargs):
        super().__init__(self.__class__.__name__, rlen=1, **kwargs)

    def analysis(self, value):
        text = ""

        if value & 0x80 == 0x80:
            text += "PEC, "
            PMBus.PEC = True
        else:
            PMBus.PEC = False

        tmp = (value & 0x60) >> 5
        if tmp == 0x00:
            text += "100KHz, "
        elif tmp == 0x01:
            text += "400KHz, "
        else:
            text += "Error Reserved, "

        if value & 0x10 == 0x10:
            text += "SMBAlert"

        return text

    def parse(self, raw):
        value = raw[0]
        return value, self.analysis(value)
