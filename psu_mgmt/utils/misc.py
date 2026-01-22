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

def parse_code(code):
    if isinstance(code, int):
        value = code

    else:
        code_str = str(code).strip().lower()

        # "0x40"
        if code_str.startswith("0x"):
            value = int(code_str, 16)

        # "40h"
        elif code_str.endswith("h"):
            value = int(code_str[:-1], 16)

        # "64"
        elif code_str.isdigit():
            value = int(code_str)

        else:
            raise ValueError(f"Invalid code format: {code}")

    if not (0 <= value <= 255):
        raise ValueError(f"Code out of range (0~255): {value}")

    return value
