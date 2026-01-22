# pylint: disable=wildcard-import
from psu_mgmt.commands.pmbus_standard import *

map_commands = { # "ClassName": ClassName,
    cls.__name__: cls for cls in (
    # PMBus Standard
        PMBus_00h_PAGE,
        PMBus_01h_OPERATION,
    )
}