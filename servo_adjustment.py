# Add automatic config modification

import excepts
from config_operations import leg_init
import time
from glob_vars import serial, legs


def calibration():
    """ Performs calibration for all legs"""
    global serial, legs

    print("Calibration starts.")
    leg_init()

    print("Basic calibration pose will be sent.")
    time.sleep(0.3)
    for i in range(6):
        for j in range(3):
            print(legs[i].sernum)
            servo = legs[i].sernum[j]
            angle = legs[i].angl_convert(j, 90)
            serial.send_1_ang(servo, angle)

    # For first servos legs are straight
    print("Coxa (closest to body) calibration starts.")
    print("Legs one by one will be straighten, check if last segment points to screw, fixing that leg.")
    for i in range(6):
        angle = legs[i].angl_convert(0, 180)    # Need to revise the procedure
        serial.send_1_ang(legs[i].sernum[0], angle)
        angle = legs[i].angl_convert(2, 90)
        print('---------- Leg', i, ' calibration. Coxa segment. Current position', angle)
        angle_adj(i, 2)
        angle = legs[i].angl_convert(0, 90)
        serial.send_1_ang(legs[i].sernum[0], angle)

    # For second servos legs are straight
    print('')
    print("Femur (middle) calibration starts.")
    print("Legs will move to refreshed basic position (all angles 90 deg),",
          "check if middle segment is horizontal.", sep='/n')

    leg_init()
    for i in range(6):
        angle = legs[i].angl_convert(1, 90)
        print('---------- Leg', i, ' calibration. Middle segment. Current position', angle)
        angle_adj(i, 1)

    # For third servos legs are straight
    print('')
    print("Tibia (outer) calibration starts.")
    print("Legs will move to basic refreshed position (all angles 90 deg),",
          "check if angle between two moving parts is 90 deg.", sep='/n')

    leg_init()
    for i in range(6):
        angle = legs[i].angl_convert(0, 90)
        print('---------- Leg', i, ' calibration. Outer segment. Current position', angle)
        angle_adj(i, 0)

    print('Calibration is finished!!!')
    return 0


def angle_adj(leg_index, segment):
    """ Asks new PWM value for servo, waits while check and corrects the config"""

    global serial, legs
    angle = 500
    servo = legs[leg_index].sernum[segment]
    while True:
        print('Enter new PWM value. For exit without saving press "q".')
        in_value = input('New PWM value: ')

        if in_value == 'q':
            return 1

        try:
            angle = int(in_value)
        except ValueError:
            print('Wrong value!')
            continue
        serial.send_1_ang(servo, angle - 200)
        serial.send_1_ang(servo, angle)
        if input('Do you need to check this position? Y/n') == 'Y':
            if position_check(servo, angle):
                modify_conf(leg_index, segment, angle)
                break
    return 0


def position_check(servo, angle, check_num=3):
    """Repeats position several times and returns True if it's OK"""
    for p in range(check_num):
        serial.send_1_ang(servo, angle + (-1) ** p * 200)
        time.sleep(1)
        serial.send_1_ang(servo, angle)
        input('Check position and press any key...')
    if input('Position is OK? (Y/n) ') == 'Y':
        return True
    return False


def modify_conf(leg_index, segment, angle):
    """ Modifies config, according to got angle"""

    import configparser
    print('Saving value...')

    config = configparser.ConfigParser()
    config.read('config.ini')

    section = 'LEG' + str(leg_index)
    if segment == 2:
        prefix = 'coxa'
    elif segment == 1:
        prefix = 'femur'
    elif segment == 0:
        prefix = 'tibia'
    else:
        raise excepts.InappropriateValue
    point_0_old = int(config[section][prefix + '_servo_0deg_point'])
    point_180_old = int(config[section][prefix + '_servo_180deg_point'])
    point_90_old = (point_180_old - point_0_old) / 2 + point_0_old
    delta = point_90_old - angle
    point_0_new = str(int(point_0_old - delta))
    point_180_new = str(int(point_180_old - delta))

    config[section][prefix + '_servo_0deg_point'] = point_0_new
    config[section][prefix + '_servo_180deg_point'] = point_180_new

    print(point_0_new, point_180_new)

    with open('copy.ini', 'w') as configfile:
        config.write(configfile)

    return 0


calibration()
