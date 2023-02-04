# New Servo test
# requires numbers on controller and positions
import time
from port import Port
from leg import Leg
from config_operations import leg_init

ser = Port()
legs = []
cycle_time = 1500
step_distance = 15
height = 3

for i in range(6):
    p = leg_init(i)
    legs.append(Leg(p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8]))

leg_list = [legs[0], legs[1], legs[2], legs[3], legs[4], legs[5]]

for i in range(6, 10, 1):
    ser.send_1_ang(i, 2500)
time.sleep(1)
for i in range(6, 10, 1):
    ser.send_1_ang(i, 1500)
time.sleep(1)
for i in range(6, 10, 1):
    ser.send_1_ang(i, 500)
time.sleep(1)
for i in range(6, 10, 1):
    ser.send_1_ang(i, 1500)

