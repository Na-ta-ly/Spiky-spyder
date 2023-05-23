# Functions for complex movements
import time

# import __main__
from movm_serv_func import get_coords_up, get_coords_fw, get_coords_down, get_coords_turn, get_coords_bw,\
    send_coord_list_legs
from glob_vars import legs, verbose


def walk(initial_coords: list, distance: int, speed=5, step=7, height=2):
    """ Walk forward for some distance
    :param initial_coords: initial coordinates for walking process
    :param distance: distance for walk
    :param speed: from 0 to 10 (0 slow, 10 fast)
    :param step: step distance
    :param height: height for leg lifting
    :return: 0
    """

    global legs
    # verbose = verbose_mode[0]

    cycle_time = int(800 - (800 - 100) / 10 * speed)  # cycle_time:[800; 100] - direct time of execution for servos
    steps = int(distance / step)

    if verbose():
        print('walk ', initial_coords)
        print(step, cycle_time)

    leg_list_1 = [legs[0], legs[4], legs[2]]  # list of legs, order VERY important!!!
    leg_list_2 = [legs[5], legs[1], legs[3]]

    # preparatory stage
    step_fw(initial_coords, [leg_list_1[0], leg_list_1[1]], step, height, cycle_time)
    move_body(initial_coords, leg_list_1, leg_list_2, step, height, cycle_time * 2)

    for i in range(steps - 1):  # sequence of steps
        step_fw(initial_coords, leg_list_2, step, height, cycle_time)
        move_body(initial_coords, leg_list_2, leg_list_1, step, height, cycle_time * 2)
        step_fw(initial_coords, leg_list_1, step, height, cycle_time)
        move_body(initial_coords, leg_list_1, leg_list_2, step, height, cycle_time * 2)

    return 0


# def turn(port: Port, legs: list, inital_coords: list, distance: int, speed=5, height=2, cycle_time=500):
#     # angle: int, leg_list: list, speed=10):
#     timer = int(800 - (800 - 100) / 10 * speed)
#     angle_new = -int(angle / 2)
#     coord = []
#     for leg in leg_list:
#         coord.append(get_coords_turn(leg.coord, angle_new, leg.ind))
#
#     send_coord_list_legs(coord, leg_list, timer)
#
#     height = 2
#     for leg in leg_list:
#         send_coord_list_legs([get_coords_up(leg.coord), height], [leg], timer)
#         input()
#         send_coord_list_legs([get_coords_turn(leg.coord, -2 * angle_new, leg.ind)], [leg], timer)
#         input()
#         send_coord_list_legs([get_coords_down(leg.coord), height], [leg], timer)
#     return 0


def pose(coord: list, leg_list: list, speed=5):  # Checked
    """ Sends coordinates to all legs in list
    :param coord: coordinates that are sent
    :param leg_list: legs
    :param speed: from 0 to 10 (0 slow, 10 fast)
    :return: 0
    """

    if verbose():
        print('Sending pose ', coord)

    cycle_time = int(800 - (800 - 100) / 10 * speed)  # cycle_time:[800; 100] - direct time of execution for servos
    for leg in leg_list:
        if coord[0] != leg.coord[0] or coord[1] != leg.coord[1]:  # check if x or y coord changed and raise leg
            send_coord_list_legs([get_coords_up(leg.coord)], [leg], cycle_time)
            send_coord_list_legs([coord], [leg], cycle_time)
        else:
            send_coord_list_legs([coord], [leg], cycle_time)
    return 0


# def rotate(port: Port, initial_coords: list, leg_list: list, angle:int, height, cycle):
#
#     for leg_x in leg_list:
#         send_coord_list_legs(port, get_coords_up(leg_x.coord, height), [leg_x], cycle)


def step_fw(initial_coords: list, leg_list: list, step, height, cycle):  #Checked
    """
    Sends leg_up, leg_forward and leg_down commands to legs in list
    :param initial_coords: initial coordinates for walking process
    :param leg_list: list legs for commands (first, second and third pair!!!)
    :param step: step distance
    :param height: height for leg lifting
    :param cycle: time for movements
    :return: 0
    """
    # global verbose_mode
    # verbose = verbose_mode[0]

    if verbose():
        print('Now is step_fw for ', leg_list)

    coor = []

    for i in range(len(leg_list)):  # move legs forward, they need to be risen
        coor.append(get_coords_fw(initial_coords, i, step))
    send_coord_list_legs(coor, leg_list, cycle)

    coor = []
    for leg_x in leg_list:  # return legs to the initial state
        coor.append(get_coords_down(leg_x.coord, height))
    send_coord_list_legs(coor, leg_list, cycle)

    return 0


def move_body(initial_coords: list, leg_list_fw: list, leg_list_bw: list, step, height, cycle_time):
    """
    Sends leg_up command to legs in leg_list_bw; and then leg_forward to leg_list_fw
    :param initial_coords:  initial coordinates for walking process
    :param leg_list_fw: list legs that are in forward position (first, second and third pair!!!)
    :param leg_list_bw: list legs that are in backward position now (first, second and third pair!!!)
    :param step: step distance
    :param height: height for leg lifting
    :param cycle_time: time for movements
    :return: 0
    """

    if verbose():
        print('move_body')
        print('Now is step_bw for ', leg_list_bw, ' and fw for ', leg_list_fw)

    coor = []
    for leg_x in leg_list_bw:
        coor.append(get_coords_up(leg_x.coord, height))
    send_coord_list_legs(coor, leg_list_bw, cycle_time)
    time.sleep(1)
    coor = []
    i = 0
    for i in range(len(leg_list_fw)):
        coor.append(get_coords_bw([initial_coords[0], initial_coords[1], initial_coords[2] - height], i, step))
    send_coord_list_legs(coor, leg_list_fw, cycle_time)
    return 0


# def turn_body(port: Port, initial_coords: list, leg_list: list, speed: int = 10):
#     """
#     Sends initial coordinates to legs in leg_list without leg lifting
#     :param port: serial port
#     :param initial_coords:  initial coordinates for walking process
#     :param leg_list_fw: list legs that are in forward position (first, second and third pair!!!)
#     :param speed: speed for movements (from 1-slow, to 10-fast)
#     :return: 0
#     """
#     timer = int(800 - (800 - 100) / 10 * speed)
#     print([initial_coords] * len(leg_list))
#     send_coord_list_legs([initial_coords] * len(leg_list), leg_list, timer)
#     return 0
#
#
# def sinle_turnport(port: Port, angle: int, leg_list: list, speed=10):
#     timer = int(800 - (800 - 100) / 10 * speed)
#     angle_new = -int(angle / 2)
#     coord = []
#     for leg in leg_list:
#         coord.append(get_coords_turn(leg.coord, angle_new, leg.ind))
#
#     send_coord_list_legs(coord, leg_list, timer)
#
#     height = 2
#     for leg in leg_list:
#         send_coord_list_legs([get_coords_up(leg.coord), height], [leg], timer)
#         input()
#         send_coord_list_legs([get_coords_turn(leg.coord, -2 * angle_new, leg.ind)], [leg], timer)
#         input()
#         send_coord_list_legs([get_coords_down(leg.coord), height], [leg], timer)
#     return 0
