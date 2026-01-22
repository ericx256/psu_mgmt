import time

from psu_mgmt.app.manager import CONF, RMDB
from psu_mgmt.drivers.r90000 import R9
from psu_mgmt.utils.misc import print_hex

def main():
    print(CONF.model_name)
    print()

    print("[commands]")
    for itr in CONF.map_commands:
        print(itr)
    print()

    print("[plugins]")
    for itr in CONF.map_plugins:
        print(itr)
    print()

    device = R9.device_path

    idx = 0
    while True:
        itr = CONF.map_commands[idx]
        print_hex(itr.read(R9, device, 0xB0))

        if idx == len(CONF.map_commands) - 1:
            idx = 0
        else:
            idx += 1

        time.sleep(0.01)

if __name__ == "__main__":
    main()
