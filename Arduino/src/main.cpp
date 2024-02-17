#include <Servo.h>
#include <Arduino.h>

Servo myservo;  // create servo object to control a servo

void setup() {
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  Serial.begin(9600); // initialize serial communication at 9600 bits per second:
}

void loop() {
  if (Serial.available() > 0) {        // check if data is available to read
    int position = Serial.parseInt();  // read the incoming integer
    if (position >= 0 && position <= 180) { // check if the position is within the servo range
      myservo.write(position);         // tell servo to go to position
    }
    Serial.println(position);          // print the position
  }
}
