# Add modifying config during adjustment
import configparser
from leg import Leg
from glob_vars import legs


def leg_init():  # Checked
    """Initiates global legs from config.ini"""

    config = configparser.ConfigParser()
    config.read('config.ini')
    list_term = ['tibia_servo_number', 'femur_servo_number', 'coxa_servo_number',
                 'tibia_servo_180deg_point', 'femur_servo_180deg_point', 'coxa_servo_180deg_point',
                 'tibia_servo_0deg_point', 'femur_servo_0deg_point', 'coxa_servo_0deg_point']
    legs.clear()
    for leg_ind in range(6):
        leg = 'LEG' + str(leg_ind)
        parametrs = []

        for param in list_term:
            parametrs.append(int(config[leg][param]))
        parametrs.append(leg_ind)
        legs.append(Leg(*parametrs))
    return 0


def get_init_coord():  # Checked
    """Returns initial coordinates from config.ini"""

    config = configparser.ConfigParser()
    config.read('config.ini')
    section_name = 'DEFAULT'
    param_name = 'default_coordinates'
    coords = config[section_name][param_name]

    init_coord = []
    i = 0
    while i <= len(coords):
        if coords[i] == ' ':
            coords = coords[i:]
            i = -1
        if coords[i] == ',':
            try:
                number = float(coords[:i])
            except ValueError:
                print('Default coordinates are wrong in config.ini!')
                return 1
            init_coord.append(number)
            coords = coords[i+2:]
            i = -1
        if i == len(coords)-1:
            try:
                number = float(coords)
            except ValueError:
                print('Default coordinates are wrong in config.ini!')
                return 1
            init_coord.append(number)
            coords = ''
        i += 1

    return init_coord
