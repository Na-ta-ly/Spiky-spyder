# Add modifying config during adjustment
import configparser
import excepts


def leg_init(leg_ind: int):
    """
    Returns from config.ini full list of parameters for a leg
    :param leg_ind: leg index
    :return: list of parameters
    """
    config = configparser.ConfigParser()
    config.read('config.ini')
    if leg_ind < 6:
        leg = 'LEG' + str(leg_ind)
    else:
        raise excepts.WrongIndex
    parametrs = []
    list_term = ['tibia_servo_number', 'femur_servo_number', 'coxa_servo_number',
                 'tibia_servo_180deg_point', 'femur_servo_180deg_point', 'coxa_servo_180deg_point',
                 'tibia_servo_0deg_point', 'femur_servo_0deg_point', 'coxa_servo_0deg_point']
    for param in list_term:
        parametrs.append(int(config[leg][param]))
    parametrs.append(leg_ind)
    return parametrs


