from port_mock import Port

serial = Port()
legs = []

verbose_mode = [False]

def verbose():
    """Returns value verbose_mode"""
    return verbose_mode[0]
