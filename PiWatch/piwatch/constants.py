class Color:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    GREY = (128, 128, 128)

    TRANSPARENT = (0, 0, 0, 0)

    @classmethod
    def from_hex(hex_str):
        """Converts a hexadecimal string to a tuple with (red, green, blue).
        Supported strings are of type, each with 8 or less hexadecimal characters:
            'hhhhhhhh'
            '#hhhhhhhh'
            '0xhhhhhhhh'
        """
        if hex_str[0] == '#':
            hex_str = hex_str[1:]
        elif hex_str[:2] == '0x':
            hex_str = hex_str[2:]
        if len(hex_str) % 2 != 0:
            hex_str = '0'+hex_str
        if len(hex_str) < 6:
            hex_str = '0'*(6-len(hex_str)) + hex_str
        return tuple(int(hex_str[i:i+2], 16) for i in range(0, len(hex_str), 2))
