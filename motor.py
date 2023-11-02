import serial
import time
class Motors:

    def __init__(self, start_pos = None):
        self.start_pos = start_pos

    def get_user_input(self):
        res = input()
        return res    

    def create_path(self, end_pos):
        start_pos = self.start_pos
        path = []
        moveX = ord(end_pos[0]) - ord(start_pos[0])
        moveY = int(end_pos[1:]) - int(start_pos[1:])
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


    def send_motor_instruction(self, direction):
        ser = serial.Serial('/dev/ttyACM0', 9600)
        ser.reset_input_buffer()

        input_str = bytes(direction + "\n")
        ser.write(input_str)
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        time.sleep(1)

    def move_along_path(self, path):
        for move in path:
            send_motor_instruction(move)


motors = Motors("A1")
print(motors.create_path("C9"))