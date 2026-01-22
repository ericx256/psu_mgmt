import builtins

from psu_mgmt.commands.pmbus_standard import PMBus

class PMBus_01h_OPERATION_(PMBus):
    def __init__(self, **kwargs):
        super().__init__(self.__class__.__name__, rlen=1, **kwargs)

    def analysis(self, value):
        text = ""

        if value & 0x80 == 0x80:
            text += "ON, "
        else:
            text += "OFF, "

        if value & 0x40 == 0x40:
            text += "Remote Shutdown, "

        return text

    def parse(self, li):
        value = li[0]
        return value, self.analysis(value)

    def apply(self, value):
        return [value]

map = {
    cls.__name__: cls for cls in (
        PMBus_01h_OPERATION_,
    )
}
builtins.map_commands.update(map)
