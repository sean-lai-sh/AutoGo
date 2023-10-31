#include <Stepper.h>

const int stepsPerRevolution = 100;
Stepper stepper1(stepsPerRevolution, 8, 9, 10, 11);



void setup() {
  stepper1.setSpeed(30);
  Serial.begin(9600);
}

void loop() {
  
  if(Serial.available() > 0){
    String data = Serial.readStringUntil('\n');
    Serial.print("You sent me: ");
    Serial.println(data);
    if(data == "A9"){
      stepper1.step(stepsPerRevolution);
    }
  }
  
}
