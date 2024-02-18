#include <Servo.h>
#include <Arduino.h>
#include <Adafruit_MotorShield.h>

#define SERVO_TURNER_MAIN_ID 0
#define SERVO_TURNER_SECONDARY_ID 1
#define MOTOR_GLASS_LEFT_ID 2
#define MOTOR_GLASS_RIGHT_ID 3

Adafruit_MotorShield AFMS = Adafruit_MotorShield();

Servo servoTurnerMain;
Servo servoTurnerSecondary;

Adafruit_DCMotor *motorGlassLeft = AFMS.getMotor(1);
Adafruit_DCMotor *motorGlassRight = AFMS.getMotor(2);

int motorGlassLeftTargetSpeed = 0;
int motorGlassRightTargetSpeed = 0;
int motorGlassLeftCurrentSpeed = 0;
int motorGlassRightCurrentSpeed = 0;

void setup() {
  Serial.begin(9600);

  if (!AFMS.begin()) {         // create with the default frequency 1.6KHz
    while (1);
  }

  motorGlassLeft->setSpeed(0);
  motorGlassRight->setSpeed(0);

  servoTurnerMain.attach(9);
  servoTurnerSecondary.attach(10);

  servoTurnerMain.write(160);
  servoTurnerSecondary.write(180);
}

void adjustMotorSpeed(Adafruit_DCMotor *motor, int &currentSpeed, int targetSpeed) {
  if (currentSpeed < targetSpeed) {
    currentSpeed++;
  } else if (currentSpeed > targetSpeed) {
    currentSpeed--;
  }
  if (currentSpeed > 0) {
    motor->run(FORWARD);
  } else if (currentSpeed < 0) {
    motor->run(BACKWARD);
  } else {
    motor->run(RELEASE);
  }
  motor->setSpeed(abs(currentSpeed));
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
      if (id == SERVO_TURNER_MAIN_ID || id == SERVO_TURNER_SECONDARY_ID) {
        if (value >= 0 && value <= 180) {
          switch (id) {
            case SERVO_TURNER_MAIN_ID:
              servoTurnerMain.write(value);
              break;
            case SERVO_TURNER_SECONDARY_ID:
              servoTurnerSecondary.write(value);
              break;
          }
        } else if (value == -1) {
          switch (id) {
            case SERVO_TURNER_MAIN_ID:
              Serial.println(servoTurnerMain.read());
              break;
            case SERVO_TURNER_SECONDARY_ID:
              Serial.println(servoTurnerSecondary.read());
              break;
          }
        }
      } else if (value >= -256 && value < 256) {
        switch (id) {
          case MOTOR_GLASS_LEFT_ID:
            motorGlassLeftTargetSpeed = value;
            break;
          case MOTOR_GLASS_RIGHT_ID:
            motorGlassRightTargetSpeed = value;
            break;
        }
      }
    }
  }

  adjustMotorSpeed(motorGlassLeft, motorGlassLeftCurrentSpeed, motorGlassLeftTargetSpeed);
  adjustMotorSpeed(motorGlassRight, motorGlassRightCurrentSpeed, motorGlassRightTargetSpeed);
}
