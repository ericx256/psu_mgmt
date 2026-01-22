from psu_mgmt.app.manager import CONF, RMDB

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

if __name__ == "__main__":
    main()
