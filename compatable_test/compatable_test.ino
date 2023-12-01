#include <Stepper.h>

const int stepsPerTick = 45;
Stepper stepper1(stepsPerTick, 8, 9, 10, 11);
Stepper stepper2(stepsPerTick, 4, 5, 6, 7);



void setup() {
  stepper1.setSpeed(100);
  stepper2.setSpeed(100);
  Serial.begin(9600);
}

void loop() {
  
  if(Serial.available() > 0){
    String data = Serial.readStringUntil('.');
    Serial.print("You sent me: ");
    Serial.println(data);
      if(data == "U"){
        stepper1.step(stepsPerTick);
      }
      if(data == "D"){
        stepper1.step(-stepsPerTick);
      }
      if(data == "L"){
        stepper2.step(stepsPerTick);
      }
      if(data == "R"){
        stepper2.step(-stepsPerTick);
      }
  }

}
