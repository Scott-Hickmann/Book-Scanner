from servo_manager import ServoManager
from servo import Servo
import time
import itertools

INITIAL_TURNER_MAIN_POSITION = 90


def calibrate(servo: Servo, initial_position, change):
    position = initial_position
    while position >= 0 and position <= 180:
        servo.set_position(position)
        time.sleep(0.1)
        # if input("Is the position good? (y/n) ") == "y":
        #     break
        position += change


if __name__ == "__main__":
    servo_manager = ServoManager()
    servoTurnerMain = Servo(0, servo_manager, INITIAL_TURNER_MAIN_POSITION)
    servoTurnerSecondary = Servo(1, servo_manager, 0)
    servoGlassLeft = Servo(2, servo_manager, 0)
    servoGlassRight = Servo(3, servo_manager, 0)

    print("Calibrating turner main")
    calibrate(servoTurnerMain, INITIAL_TURNER_MAIN_POSITION, change=-10)
    servoTurnerMain.initial_position = servoTurnerMain.position
    print("Calibrating turner secondary")
    calibrate(servoTurnerSecondary, 0, change=10)
    servoTurnerSecondary.initial_position = servoTurnerSecondary.position

    servoTurnerMain.reset()
    servoTurnerSecondary.reset()
    for i in itertools.count():
        print(f"Starting page {i}")
        servoTurnerMain.glide_position(140, speed=3)
        servoTurnerSecondary.glide_position(60, speed=5)
        servoTurnerMain.glide_position(servoTurnerMain.initial_position, speed=5)
        servoTurnerSecondary.glide_position(
            servoTurnerSecondary.initial_position, speed=5
        )
        print(f"Finished page {i}")

    # try:
    #     while True:
    #         position = int(input("Enter position: "))
    #         servoTurnerMain.set_position(position)
    #         servoTurnerSecondary.set_position(position)
    #         servoGlassLeft.set_position(position)
    #         servoGlassRight.set_position(position)
    #         print(
    #             f"{servoTurnerMain.get_position()} {servoTurnerSecondary.get_position()} {servoGlassLeft.get_position()} {servoGlassRight.get_position()}"
    #         )
    # finally:
    #     servo_manager.arduino.close()
