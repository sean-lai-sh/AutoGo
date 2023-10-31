#include <Stepper.h>

const int stepsPerRevolution = 100;
Stepper stepperX(stepsPerRevolution, 8, 9, 10, 11);
Stepper stepperY(stepsPerRevolution, 4, 5, 6, 7);


void setup() {
  stepperX.setSpeed(30);
  stepperY.setSpeed(30);
  Serial.begin(9600);
}

void loop() {
  
  if(Serial.available() > 0){
    String data = Serial.readStringUntil('\n');
    if(data == "up"){
        stepperX.step(stepsPerRevolution);
    }
    if(data == "down"){
        stepperX.step(-stepsPerRevolution);
    }
    if(data == "left"){
        stepperY.step(stepsPerRevolution);
    }
    if(data == "right"){
        stepperY.step(-stepsPerRevolution);
    }
  }
  
}