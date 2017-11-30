#include <Servo.h>

const int SERVO_0_PIN = 3;

Servo servo_0;  // create servo object to control a servo

void setup() {
  servo_0.attach(SERVO_0_PIN);  // attaches the servo on pin 9 to the servo object
  Serial.begin(9600);
}

void loop() {
  String msg; 
  if (Serial.available() > 0) {
    // read the incoming string:
    msg = Serial.readString();
    // Parse string and convert into ints
    int angle_0 = msg.substring(0,3).toInt();
    
    // Write to servos incoming angles
    servo_0.write(angle_0);
  }
}
