import serial
import time

def get_user_input():
    res = input()
    return res    

def create_path(start_pos, end_pos):
    path = []
    moveX = ord(end_pos[0]) - ord(start_pos[0])
    moveY = int(end_pos[1:]) - int(start_pos[1:])
    while moveX < 0:
        path.append("up")
        moveX += 1
    while moveX > 0:
        path.append("down")
        moveX -= 1

    while moveY < 0:
        path.append("left")
        moveY += 1
    while moveY > 0:
        path.append("right")
        moveY -= 1
    return path


def send_motor_instruction(direction):
    ser = serial.Serial('/dev/ttyACM0', 9600)
    ser.reset_input_buffer()

    input_str = bytes(direction + "\n")
    ser.write(input_str)
    line = ser.readline().decode('utf-8').rstrip()
    print(line)
    time.sleep(1)

def move_along_path(path):
    for move in path:
        send_motor_instruction(move)


print(create_path("A1", "C9"))