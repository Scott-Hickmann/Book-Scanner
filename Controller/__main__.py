from servo_manager import ServoManager
from servo import Servo

if __name__ == "__main__":
    servo_manager = ServoManager()
    servoTurnerMain = Servo(0, servo_manager)
    servoTurnerSecondary = Servo(1, servo_manager)
    servoGlassLeft = Servo(2, servo_manager)
    servoGlassRight = Servo(3, servo_manager)

    try:
        while True:
            position = int(input("Enter position: "))
            servoTurnerMain.set_position(position)
            servoTurnerSecondary.set_position(position)
            servoGlassLeft.set_position(position)
            servoGlassRight.set_position(position)
    finally:
        servo_manager.arduino.close()
