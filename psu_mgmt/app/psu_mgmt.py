import time

from psu_mgmt.app.manager import CONF, RMDB
from psu_mgmt.drivers.driver import Driver

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

    driver = Driver()

    idx = 0
    while True:
        itr = CONF.map_commands[idx]
        print(itr.read(driver, "", 0xB0))

        if idx == len(CONF.map_commands) - 1:
            idx = 0
        else:
            idx += 1

        time.sleep(0.01)

if __name__ == "__main__":
    main()
