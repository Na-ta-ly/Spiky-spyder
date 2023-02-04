# Functions for complex movements
import time
from port import Port
from leg import Leg
from movm_serv_func import get_coords_up, get_coords_fw, get_coords_down, get_coords_turn, get_coords_bw,\
    send_coord_list_legs


def walk(port: Port, legs: list, inital_coords: list, distance: int, speed=5, step_distance=7,
         height=2, cycle_time=500):
    step_distance = int(step_distance / 12*speed)+2
    cycle_time = int(800 - (800-100)/10 * speed)
    print(step_distance, cycle_time)
    leg_list_1 = [legs[0], legs[4], legs[2]]  # list of legs, order VERY important!!!
    leg_list_2 = [legs[5], legs[1], legs[3]]
    steps = int(distance / step_distance)
    print(steps, step_distance, cycle_time)
    step_fw(port, inital_coords, [leg_list_1[0], leg_list_1[1]], step_distance, height, cycle_time)
    move_body(port, inital_coords, leg_list_1, leg_list_2, step_distance, height, cycle_time*2)
    for i in range(steps-1):
        step_fw(port, inital_coords, leg_list_2, step_distance, height, cycle_time)
        move_body(port, inital_coords, leg_list_2, leg_list_1, step_distance, height, cycle_time*2)
        step_fw(port, inital_coords, leg_list_1, step_distance, height, cycle_time)
        move_body(port, inital_coords, leg_list_1, leg_list_2, step_distance, height, cycle_time*2)

    # for i in range(steps):
    #     step_fw(port, inital_coords, leg_list_1, step_distance, height, cycle_time)
    #     move_body(port, inital_coords, leg_list_1, leg_list_2, step_distance, height, cycle_time)
    #     step_fw(port, inital_coords, leg_list_2, step_distance, height, cycle_time)
    #     move_body(port, inital_coords, leg_list_2, leg_list_1, step_distance, height, cycle_time)
    # if steps % 2:
    #     step_fw(port, inital_coords, leg_list_1, step_distance, height, cycle_time)
    #     move_body(port, inital_coords, leg_list_1, leg_list_2, step_distance, height, cycle_time)


def turn(port: Port, angle: int, leg_list: list, speed=10):
    timer = int(800 - (800-100)/10 * speed)
    angle_new = -int(angle/2)
    coord = []
    for leg in leg_list:
        coord.append(get_coords_turn(leg.coord, angle_new, leg.ind))

    send_coord_list_legs(port, coord, leg_list, timer)

    height = 2
    for leg in leg_list:
        send_coord_list_legs(port, [get_coords_up(leg.coord), height], [leg], timer)
        input()
        send_coord_list_legs(port, [get_coords_turn(leg.coord, -2*angle_new, leg.ind)], [leg], timer)
        input()
        send_coord_list_legs(port, [get_coords_down(leg.coord), height], [leg], timer)
    return 0



def pose(port: Port, coord: list, leg_list: list, speed=10):
    timer = int(800 - (800-100)/10 * speed)
    #i = len(leg_list)
    for leg in leg_list:
        #print(coord[0], leg.coord[0], coord[1], leg.coord[1])
        if coord[0] != leg.coord[0] or coord[1] != leg.coord[1]:
            send_coord_list_legs(port, [get_coords_up(leg.coord)], [leg], timer)
            send_coord_list_legs(port, [coord], [leg], timer)
        else:
            send_coord_list_legs(port, [coord], [leg], timer)
    return 0


# def rotate(port: Port, initial_coords: list, leg_list: list, angle:int, height, cycle):
#
#     for leg_x in leg_list:
#         send_coord_list_legs(port, get_coords_up(leg_x.coord, height), [leg_x], cycle)


def step_fw(port: Port, initial_coords: list, leg_list: list, step, height, cycle):
    """
    Sends leg_up, leg_forward and leg_down commands to legs in list
    :param port: serial port
    :param initial_coords: initial coordinates for walking process
    :param leg_list: list legs for commands (first, second and third pair!!!)
    :param step: step distance
    :param height: height for leg lifting
    :param cycle: time for movements
    :return: 0
    """
    print('Now is step_fw')
    coor = []
    i = 0
    for leg_x in leg_list:
        coor.append(get_coords_fw(initial_coords, i, step))
        i += 1
    #print(coor)
    send_coord_list_legs(port, coor, leg_list, cycle)
    coor = []
    for leg_x in leg_list:
        coor.append(get_coords_down(leg_x.coord, height))
    send_coord_list_legs(port, coor, leg_list, cycle)
    return 0


def move_body(port: Port, initial_coords: list, leg_list_fw: list, leg_list_bw: list, step, height, cycle_time):
    """
    Sends leg_up command to legs in leg_list_bw; and then leg_forward to leg_list_fw
    :param port: serial port
    :param initial_coords:  initial coordinates for walking process
    :param leg_list_fw: list legs that are in forward position (first, second and third pair!!!)
    :param leg_list_bw: list legs that are in backward position now (first, second and third pair!!!)
    :param step: step distance
    :param height: height for leg lifting
    :param cycle_time: time for movements
    :return: 0
    """
    print('Now is step_bw')
    coor = []
    for leg_x in leg_list_bw:
        coor.append(get_coords_up(leg_x.coord, height))
    send_coord_list_legs(port, coor, leg_list_bw, cycle_time)
    time.sleep(1)
    coor = []
    i = 0
    for leg_x in leg_list_fw:
        coor.append(get_coords_bw([initial_coords[0], initial_coords[1], initial_coords[2]-height], i, step))
        # print('Leg' + i, coor)
        i += 1
    #print(coor)
    send_coord_list_legs(port, coor, leg_list_fw, cycle_time)
    return 0


def turn_body(port: Port, initial_coords: list, leg_list: list, speed: int = 10):
    """
    Sends initial coordinates to legs in leg_list without leg lifting
    :param port: serial port
    :param initial_coords:  initial coordinates for walking process
    :param leg_list_fw: list legs that are in forward position (first, second and third pair!!!)
    :param speed: speed for movements (from 1-slow, to 10-fast)
    :return: 0
    """
    timer = int(800 - (800-100)/10 * speed)
    print([initial_coords]*len(leg_list))
    send_coord_list_legs(port, [initial_coords]*len(leg_list), leg_list, timer)
    return 0
