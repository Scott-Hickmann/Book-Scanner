#include <Servo.h>
#include <Arduino.h>

#define SERVO_TURNER_MAIN_ID 0
#define SERVO_TURNER_SECONDARY_ID 1
#define SERVO_GLASS_LEFT_ID 2
#define SERVO_GLASS_RIGHT_ID 3

Servo servoTurnerMain;
Servo servoTurnerSecondary;
Servo servoGlassLeft;
Servo servoGlassRight;

void setup() {
  Serial.begin(9600);

  servoTurnerMain.attach(5);
  servoTurnerSecondary.attach(6);
  servoGlassLeft.attach(9);
  servoGlassRight.attach(10);

  servoTurnerMain.write(20);
  servoTurnerSecondary.write(180);
  servoGlassLeft.write(0);
  servoGlassRight.write(180);
}

void loop() {
  if (Serial.available() > 0) {
    // Read the incoming string until newline is received
    String inputString = Serial.readStringUntil('\n');
    // Expecting input format as id,value
    int commaIndex = inputString.indexOf(',');
    if (commaIndex != -1) {
      int id = inputString.substring(0, commaIndex).toInt();
      int value = inputString.substring(commaIndex + 1).toInt();
      if (value >= 0 && value <= 180) {
        switch (id) {
          case SERVO_TURNER_MAIN_ID:
            servoTurnerMain.write(value);
            break;
          case SERVO_TURNER_SECONDARY_ID:
            servoTurnerSecondary.write(value);
            break;
          case SERVO_GLASS_LEFT_ID:
            servoGlassLeft.write(value);
            break;
          case SERVO_GLASS_RIGHT_ID:
            servoGlassRight.write(value);
            break;
        }
      } else if (value == -1) { // Get value
        switch (id) {
          case SERVO_TURNER_MAIN_ID:
            Serial.println(servoTurnerMain.read());
            break;
          case SERVO_TURNER_SECONDARY_ID:
            Serial.println(servoTurnerSecondary.read());
            break;
          case SERVO_GLASS_LEFT_ID:
            Serial.println(servoGlassLeft.read());
            break;
          case SERVO_GLASS_RIGHT_ID:
            Serial.println(servoGlassRight.read());
            break;
        }
      }
    }
  }
}
