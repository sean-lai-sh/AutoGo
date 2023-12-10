#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_PWMServoDriver.h"

Adafruit_MotorShield motor_control = Adafruit_MotorShield();
const int SPR = 200
const int speed = 35
Adafruit_StepperMotor *motor1 = motor_conrtol.getStepper(SPR, 1); // Change to proper Steps Per Revolution
Adafruit_StepperMotor *motor2 = motor_control.getStepper(SPR, 2);

void setup(){
    motor1->setSpeed(speed)
    motor2->setSpeed(speed)

}

void loop(){
    motor1->step(15, FORWARD, SINGLE)
    delay(1000)
    motor1->step(15, BACKWARD, SINGLE)
}