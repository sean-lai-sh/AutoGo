import serial
import time

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout = 1)
    ser.reset_input_buffer()

    cond = True

    while cond is True:
        ser.write(b"hi from pi\n")
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        time.sleep(1)