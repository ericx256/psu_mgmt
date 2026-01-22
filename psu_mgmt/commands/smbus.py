class SMBus:
    def __init__(self):
        self.name = ""
        self.code = 0x00

        self.rlen = 0
        self.r_wbuf = []

        self.raw = "" # "B079-B10000FF"
        self.value = "" # "12.2"

        self.enabled = True

    def __str__(self):
        return f"{self.code=:02X}h, {self.name=}, {self.rlen=}"
