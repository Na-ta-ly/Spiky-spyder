import serial
from excepts import NotEnoughParams

class Port(serial.Serial):
# class Port():

    REPETITIONS = 2  # repetitions for a servo

    def __init__(self):
        super().__init__(port="/dev/ttyS0", baudrate=9600, parity=serial.PARITY_NONE,
                         stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)

    def _send_string(self, string):
        if self.is_open:
            for m in range(self.REPETITIONS):
                self.write(string.encode('ascii'))
        else:
            return 1
        return 0

    # def send_3_ang(self, servos: list, values: list, time=500):
    #     """
    #     Sends 3 new values to 3 servos
    #     :param servos: list of servos' numbers
    #     :param values: list of converted angles
    #     :param time: optional (500)
    #     :return: 0
    #     """
    #     string = ''
    #     for i in range(3):
    #         string = string + '#' + str(servos[i]) + 'P' + str(values[i])
    #     string = string + 'T' + str(time) + '\r\n'
    #     print(string)
    #     self._send_string(string)
    #     return 0

    def send_1_ang(self, servo: int, value: int, time=500):
        """
        Sends 1 new values to a servo
        :param servo: servo number
        :param value: converted angle
        :param time: optional (500)
        :return: 0
        """
        string = '#' + str(servo) + 'P' + str(value) + 'T' + str(time) + '\r\n'
        # print(string)
        self._send_string(string)
        return 0

    def send_list_ang(self, servos: list, values: list, time=500):
        """
        Sends new values to a list of servos
        :param servos: list of servos' numbers
        :param values: list of duty cycles
        :param time: optional (500)
        :return: 0
        """
        string = ''
        if len(servos) != len(values):
            raise NotEnoughParams
        for i in range(len(servos)):
            for j in range(3):
                string = string + '#' + str(servos[i][j]) + 'P' + str(values[i][j])
        string = string + 'T' + str(time) + '\r\n'
        # print(string)
        self._send_string(string)
        return 0
