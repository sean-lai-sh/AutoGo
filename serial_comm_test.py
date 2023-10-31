import serial
import time

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600)
    ser.reset_input_buffer()
    
    cond = True
    
    while cond == True:
#        if ser.in_waiting > 0:
#            line = ser.readline().decode('utf-8').rstrip()
#            print(line)
        input_str = raw_input("put something here: ")
        input_str = bytes(input_str + "\n")
        ser.write(input_str)
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        time.sleep(1)