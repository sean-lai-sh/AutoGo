#include <Stepper.h>

const int stepsPerRevolution = 100;
Stepper stepper1(stepsPerRevolution, 8, 9, 10, 11);



void setup() {
  stepper1.setSpeed(30);
  Serial.begin(9600);
}

void loop() {
  
  if(Serial.available() > 0){
    String data = Serial.readStringUntil('.');
    Serial.print("You sent me: ");
    Serial.println(data);
    
  }
  
}
