from .smbus import SMBus

class PMBus(SMBus):
    PEC = False # PMBus_19h
    VOUT_MODE = None # PMBus_20h

    def __init__(self, class_name="", code=None, page=None, enabled=True, **_):
        super().__init__()
