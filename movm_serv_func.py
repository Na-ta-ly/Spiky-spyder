# Functions for counting coordinates and angles
# +send_coord_list_legs
import numpy as np
from port import Port
from excepts import InappropriateValue, WrongIndex


def get_angles(x: float, y: float, z: float):
    """ Converts given x,y,z into angles for legs
    :param x: distance from body (femur center)
    :param y: distance forward-backward (without the correction for tibia)
    :param z: height (femur center)
    :return: list, 'raw' angles from the tibia to the coxa
    """
    dx = 3  # tibia bending
    dy = 2.75  # distance from coxa to femur
    dz = 4  # height of femur
    k = 8.5  # femur
    m = 14.5  # tibia
    raw_x = x
    x = x - dx #- dy
    y = y
    z = z #- dz
    oa = np.sqrt(x ** 2 + z ** 2)
    p = (k ** 2 + oa ** 2 - m ** 2)/(2 * k * oa)
    #q = x / oa
    s = (m ** 2 + k ** 2 - oa ** 2) / (2 * k * m)
    if (p < -1) or (p > 1) or (s < -1) or (s > 1):
        raise InappropriateValue
    if y >= 0:
        coxa = y / raw_x
        angle_coxa = int(np.degrees(np.arctan(coxa))) + 90
    else:
        coxa = raw_x / np.abs(y)
        angle_coxa = int(np.degrees(np.arctan(coxa)))
    if z >= 0:
        angle_femur_2 = np.arctan(z/x) + np.pi/2
    else:
        angle_femur_2 = np.arctan(x/np.abs(z))
    angle_femur_1 = np.arccos(p)
    angle_femur = int(np.degrees(angle_femur_1 + angle_femur_2))
    angle_tibia = int(np.degrees(np.arccos(s)))
    return [angle_tibia, angle_femur, angle_coxa]


def get_coords_up(coords: list, height: float = 2, zero_level=-10) -> list:
    """
    Returns new coordinates for lifted leg position
    :param zero_level: initial z
    :param coords: current coordinates
    :param height: height
    :return: new coordinates
    """
    if height <= 0:
        raise InappropriateValue
    return [coords[0], coords[1], coords[2] + height]#zero_level+height]


def get_coords_down(coords: list, height: float = 2, zero_level=-10) -> list:
    """
    Returns new coordinates for putting down lifted leg
    :param zero_level:
    :param coords: current coordinates
    :param height: height
    :return: new coordinates
    """
    if height <= 0:
        raise InappropriateValue
    return [coords[0], coords[1], coords[2] - height]

#    return [coord[0], coord[1], zero_level-height]


def get_coords_fw(coords: list, leg_indx: int, step: float) -> list:
    """
    Returns new coordinates for forward position, depending on leg type and step
    Order in leg-list VERY important: indexing depends on leg's position (first, second and third pair)!!!
    :param coords: initial coordinates
    :param leg_indx: index the leg
    :param step: step distance
    :return: new coordinates
    """
    if leg_indx > 5:
        raise WrongIndex
    d = step / 2
    if leg_indx == 0 or leg_indx == 5:  # first pair
        return [np.sqrt(np.power(d, 2)-np.power(0.5*d, 2)) + coords[0], d / 2, coords[2]]
    if leg_indx == 1 or leg_indx == 4:  # middle pair
        return [coords[0], d, coords[2]]
    if leg_indx == 2 or leg_indx == 3:  # last pair
        return [coords[0] - np.sqrt(np.power(d, 2) - np.power(0.5 * d, 2)), -d / 2, coords[2]]


def get_coords_bw(coords: list, leg_indx: int, step: float) -> list:
    """
    Returns new coordinates for backward position, depending on leg type and step
    Order in leg-list VERY important: indexing depends on leg's position (first, second and third pair)!!!
    :param coords: initial coordinates
    :param leg_indx: index the leg
    :param step: step distance
    :return: new coordinates
    """
    if leg_indx > 5:
        raise WrongIndex
    d = step / 2
    if leg_indx == 0 or leg_indx == 5:  # first pair
        return [-np.sqrt(np.power(d, 2)-np.power(0.5*d, 2)) + coords[0], -d / 2, coords[2]]
    if leg_indx == 1 or leg_indx == 4:  # middle pair
        return [coords[0], -step / 2, coords[2]]
    if leg_indx == 2 or leg_indx == 3:  # last pair
        return [coords[0] + np.sqrt(np.power(d, 2) - np.power(0.5 * d, 2)), d / 2, coords[2]]


def send_coord_list_legs(ser: Port, coords: list, leg_list: list, cycle_time=500):
    """
    Sends coordinates from list to legs in list
    :param cycle_time:
    :param coords: list of coordinates
    :param ser: port
    :param leg_list: list of legs
    :return: 0
    """
    servos_list = []
    ang_list = []
    i = 0
    for leg_x in leg_list:
        servos_list.append(leg_x.sernum)
        ang_list.append(leg_x.angl_convert_3(get_angles(coords[i][0], coords[i][1], coords[i][2])))
        leg_x.set_new_coord(coords[i])
        #print(coords[i])
        i += 1
    ser.send_list_ang(servos_list, ang_list, cycle_time)
    return 0


# def get_distance(coord_1: list, coord_2: list) -> float:
#     """
#     Returs the distance between 2 points
#     :param coord_1: coordinates point 1
#     :param coord_2: coordinates point 2
#     :return: distance
#     """
#     return np.sqrt(np.power(coord_1[0] - coord_2[0], 2) + np.power(coord_1[1]-coord_2[1], 2))

def get_coords_turn(coords: list, angle: float, leg_index: int) -> list:
    """
    Returns new coordinates for turn,
    :param coords: list of coordinates
    :param angle: target angle in degrees
    :param leg_index: index
    :return: new coordinates
    """
    sign = 1
    if leg_index >2:
        sign = -sign
    #print(angle)
    l = np.sqrt(np.power(coords[0], 2) + np.power(coords[1], 2))
    y2 = l * np.sin(np.radians(angle))
    x2 = l * np.cos(np.radians(angle))
    print([x2, sign*y2, coords[2]])
    return [x2, sign*y2, coords[2]]


