# CRC8

CRC8_CCITT = 0x107
def calc_crc8(li, poly=CRC8_CCITT, init=0x0000):
    crc = init
    for byte in li:
        crc ^= byte
        for _ in range(8):
            if crc & 0x80 != 0:
                crc <<= 1
                crc ^= poly
            else:
                crc <<= 1
    return crc & 0xFF

# CRC16

CRC16_IBM_REV = 0xA001
def calc_crc16(li, poly=CRC16_IBM_REV, init=0x0000):
    crc = init
    for byte in li:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc >>= 1
                crc ^= poly
            else:
                crc >>= 1
    return crc & 0xFFFF

CRC16_IBM_REV_TABLE = [
    0x0000, 0xCC01, 0xD801, 0x1400, 0xF001, 0x3C00, 0x2800, 0xE401,
    0xA001, 0x6C00, 0x7800, 0xB401, 0x5000, 0x9C01, 0x8801, 0x4400
]
def calc_crc16t(li, init=0x0000, table=None):
    if table is None:
        table = CRC16_IBM_REV_TABLE

    crc = init
    for byte in li:
        # low 4 bits
        r = table[crc & 0xF]
        crc = (crc >> 4) & 0x0FFF
        crc = crc ^ r ^ table[byte & 0xF]

        # high 4 bits
        r = table[crc & 0xF]
        crc = (crc >> 4) & 0x0FFF
        crc = crc ^ r ^ table[(byte >> 4) & 0xF]
    return crc & 0xFFFF

def generate_crc16_rev_table(poly=0xA001):
    table = []
    for i in range(16):  # 0x0 到 0xF
        crc = i  # 初始化 CRC
        for _ in range(4):  # 處理 4 位
            if crc & 0x1:  # 如果最低位是 1
                crc = (crc >> 1) ^ poly
            else:
                crc >>= 1
        table.append(crc & 0xFFFF)  # 確保是 16 位
    return table
