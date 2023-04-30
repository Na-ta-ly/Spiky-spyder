import excepts


class Leg:
    def __init__(self, servo_tibia, servo_femur, servo_coxa,
                 ang_180_tibia, ang_180_femur, ang_180_coxa,
                 ang_0_tibia, ang_0_femur, ang_0_coxa, indx, x=0., y=0., z=0.):
        self.sernum = [servo_tibia, servo_femur, servo_coxa]
        self.coord = [x, y, z]
        self.ang_180 = [ang_180_tibia, ang_180_femur, ang_180_coxa]
        self.ang_0 = [ang_0_tibia, ang_0_femur, ang_0_coxa]
        self.ind = indx

    def set_new_coord(self, coords: list):
        for k in range(3):
            self.coord[k] = coords[k]

    def get_cur_coord(self) -> list:
        return self.coord

    def angl_convert(self, seg_ind, counted_angl):
        """
        Converts angles from degrees into duty cycle
        :param seg_ind: segment number
        :param counted_angl: angle value, in degrees
        :return: duty cycle
        """
        angl_180 = self.ang_180[seg_ind]
        angl_0 = self.ang_0[seg_ind]
        new_angl = int(((angl_180 - angl_0)/180 * counted_angl) + angl_0)
        return new_angl

    def angl_convert_3(self, counted_angls: list):
        """
        Converts list of 3 angels in degrees in duty cycle
        :param counted_angls: angles in degrees
        :return: list of converted angles
        """
        new_list = []
        for i in range(3):
            new_list.append(self.angl_convert(i, int(counted_angls[i])))
        return new_list
