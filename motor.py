import serial
import time
from go_processing import from_gtp
class Motors:

    def __init__(self, start_pos = None, size = 9):
        self.start_pos = start_pos
        self.board_size = size
        self.ser = serial.Serial('/dev/ttyACM0', 9600)
        self.ser.reset_input_buffer()

    def get_user_input(self):
        res = input()
        return res    

    def create_path(self, end_pos):
        start_pos = self.start_pos
        path = []
        move = from_gtp(end_pos, self.board_size)
        moveX = move[0]
        moveY = move[1]
        while moveX < 0:
            path.append("U")
            moveX += 1
        while moveX > 0:
            path.append("D")
            moveX -= 1

        while moveY < 0:
            path.append("L")
            moveY += 1
        while moveY > 0:
            path.append("R")
            moveY -= 1
        return path

    def move(self, end_pos):
        p = self.create_path(end_pos)
        self.move_along_path(p)
        return 1
    def send_motor_instruction(self, direction):
        self.ser.reset_input_buffer()
        input_str = bytes(direction + "\n")
        self.ser.write(input_str)
        line = self.ser.readline().decode('utf-8').rstrip()
        print(line)
        time.sleep(1)

    def close(self):
        self.ser.close()
    def move_along_path(self, path):
        for move in path:
            self.send_motor_instruction(move)

    def multi_move(self, lst_moves):
        # To be implemented @il.ydna
        pass



motors = Motors("A1")
print(motors.create_path("C9"))