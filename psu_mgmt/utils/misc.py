def print_hex(raw):
    for itr in raw:
        print(f"{itr:02X} ", end="")
    print()

def string_hex(raw):
    string = ""
    for itr in raw:
        string += f"{itr:02X} "
    return string

def string_hex_addr(raw, file_path=""):
    text = ""
    for idx, itr in enumerate(raw):
        if idx % 16 == 0:
            text += f"{idx:08X}: "

        text += f"{itr:02X} "

        if idx % 16 == 15:
            text += "\n"

    if file_path:
        with open(file_path, "w") as fp:
            fp.write(text)

    return text
