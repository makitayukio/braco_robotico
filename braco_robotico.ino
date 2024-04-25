#include <Stepper.h>
#include <Servo.h>
#include <string.h>

#define STEPPER_SPEED 10 // rpm

#define STEPS 2048 // constant

Stepper angle(STEPS, 14, 16, 15, 17); // angle base
Stepper arm(STEPS,  5,  3,  4,  2); // vert arm
Stepper base(STEPS,  9,  7,  8,  6); // vert base

Servo servo1;

String received;

int claw_mov = 10;
int angle_mov = 0;
int base_mov = 0;
int arm_mov = 0;

void setup() {
  Serial.begin(115200);

  angle.setSpeed(STEPPER_SPEED);
  arm.setSpeed(STEPPER_SPEED);
  base.setSpeed(STEPPER_SPEED);

  servo1.attach(10);
}

void loop() {
  received = Serial.readString();

  parseData();

  servo1.write(claw_mov);
  angle.step(angle_mov);
  base.step(base_mov);
  arm.step(arm_mov);

  // Serial.println("" + String(claw_mov) + "," + String(angle_mov) + "," + String(base_mov) + "," + String(arm_mov) + "");

  // delay((10*60000)/(STEPPER_SPEED*STEPS)); // 10 comes from the controller, 60000 is the transformation from minutes to ms 
}

void parseData() {
  char commands[14];
  
  received.toCharArray(commands, 14);

  char * index;
  index = strtok(commands, ",");

  while(index != NULL) {
    claw_mov = atoi(index);
    index = strtok(NULL, ",");

    angle_mov = atoi(index);
    index = strtok(NULL, ",");

    base_mov = atoi(index);
    index = strtok(NULL, ",");

    arm_mov = atoi(index);
    index = strtok(NULL, ",");
  }
}
