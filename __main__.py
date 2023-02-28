#!/usr/bin/python3
import time
from func_steps import pose, walk, turn, turn_body
from port import Port
from leg import Leg
from movm_serv_func import send_coord_list_legs
from config_operations import leg_init

ser = Port()
legs = []
cycle_time = 200
step_distance = 7
height = 3


for i in range(6):
    p = leg_init(i)
    legs.append(Leg(p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9]))

leg_list = [legs[0], legs[1], legs[2], legs[3], legs[4], legs[5]]
leg_list_1 = [legs[0], legs[4], legs[2]]  #list of legs, order VERY important!!!
leg_list_2 = [legs[5], legs[1], legs[3]]

"""for i in range(6):
    print(legs[i].coord, legs[i].sernum, legs[i].ang_180, legs[i].ang_0, legs[i].ind)"""
initial_coords = [5, 0, -7]
for i in range(6):
    legs[i].set_new_coord(initial_coords)
#print(legs[2].get_cur_coord())
pose(ser, initial_coords, leg_list)
time.sleep(3)

#walk(ser, legs, initial_coords, 40, speed=10)

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