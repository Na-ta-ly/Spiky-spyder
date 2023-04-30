#!/usr/bin/python3
import time
from func_steps import pose, walk, turn, turn_body
# from port_mock import Port
# from leg import Leg
# from movm_serv_func import send_coord_list_legs
from config_operations import leg_init, get_init_coord
from glob_vars import *


def main():
    global serial
    global legs
    global verbose_mode
    # cycle_time = 200
    step_distance = 7
    height = 3
    leg_init()

    verbose_mode[0] = True

    '''Legs order:
    0 - right first, 2 - right third;
    5 - left first, 3 - left third'''

    leg_list = [legs[0], legs[5], legs[1], legs[4], legs[2], legs[3]]
    leg_list_1 = [legs[0], legs[4], legs[2]]  #list of legs, order VERY important!!!
    leg_list_2 = [legs[5], legs[1], legs[3]]

    initial_coords = get_init_coord()
    if verbose():
        print('Sending initial pose ', initial_coords)

    for i in range(6):  # need to initiate coordinates after legs initiation
        legs[i].set_new_coord(initial_coords)

    pose(initial_coords, leg_list)
    time.sleep(3)

    if verbose():
        print('Walking ')
    walk(initial_coords, 40, speed=5)

    #pose(ser, initial_coords, leg_list)
    #turn(ser, 40, leg_list, 3)
    #turn_body(ser, initial_coords, leg_list, 3)
    #pose(ser, initial_coords, leg_list)

    #for i in range(3):
    #    turn(ser, 20, leg_list)
    #    turn_body(ser, initial_coords, leg_list, 3)
    #for i in range(3):
    #    turn(ser, -20, leg_list)
    #    turn_body(ser, initial_coords, leg_list, 5)
    #pose(ser, initial_coords, leg_list)

    return 0


main()
