# Add automatic config modification
from port import Port
from leg import Leg
from config_operations import leg_init

ser = Port()
legs = []

for i in range(6):
    p = leg_init(i)
    legs.append(Leg(p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8]))

for i in range(6):
    for j in range(3):
        servo = legs[i].sernum[j]
        angle = legs[i].angl_convert(j, 90)
        ser.send_1_ang(servo, angle)

leg_ind = 5
seg_ind = 0
servo = legs[leg_ind].sernum[seg_ind]
print(leg_ind, seg_ind, servo)
print(legs[leg_ind].angl_convert(seg_ind, 90))

while True:
    x = int(input('Enter angle '))
    ser.send_1_ang(servo, x)
