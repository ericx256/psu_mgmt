from .pmbus import PMBus

class PMBus_00h_PAGE(PMBus):
    def __init__(self, **kwargs):
        super().__init__(self.__class__.__name__, **kwargs)
        self.length = 1

    def parse(self, li):
        value = li[0]
        self.set_text(f"Page {value}")
