from servo_manager import ServoManager
from servo import Servo, InvertedServo
from joined_servo import JoinedServo
import time
import itertools

INITIAL_TURNER_MAIN_POSITION = 90


def calibrate(servo: Servo, initial_position, change):
    position = initial_position
    while position >= 0 and position <= 180:
        servo.set_position(position)
        time.sleep(0.1)
        if input("Is the position good? (y/n) ") == "y":
            break
        position += change


if __name__ == "__main__":
    try:
        servo_manager = ServoManager()
        servoTurnerMain = Servo(0, servo_manager, INITIAL_TURNER_MAIN_POSITION)
        servoTurnerSecondary = Servo(1, servo_manager, 0)
        servoGlassLeft = Servo(2, servo_manager, 0)
        servoGlassRight = InvertedServo(3, servo_manager, 0)
        servoGlass = JoinedServo([servoGlassLeft, servoGlassRight])

        servoTurnerMain.glide_position(0, speed=5)  # So that the glass doesn't hit it

        print("Calibrating glass")
        calibrate(servoGlass, 0, change=10)
        servoGlass.initial_position = servoGlass.get_position()

        servoTurnerMain.glide_position(INITIAL_TURNER_MAIN_POSITION, speed=5)
        servoTurnerSecondary.glide_position(0, speed=5)

        print("Calibrating turner main")
        calibrate(servoTurnerMain, INITIAL_TURNER_MAIN_POSITION, change=-10)
        servoTurnerMain.initial_position = servoTurnerMain.get_position()

        print("Calibrating turner secondary")
        calibrate(servoTurnerSecondary, 0, change=10)
        servoTurnerSecondary.initial_position = servoTurnerSecondary.get_position()

        print("Calibration finished")

        servoTurnerMain.glide_position(servoTurnerMain.initial_position, speed=3)
        servoTurnerSecondary.glide_position(
            servoTurnerSecondary.initial_position, speed=5
        )
        servoGlass.glide_position(0, speed=5)
        for i in itertools.count():
            print(f"Starting page {i}")
            # 1. Turn the page
            servoTurnerMain.glide_position(140, speed=3)
            # 2. Release the page
            servoTurnerSecondary.glide_position(60, speed=5)
            # 3. Bring the glass down to flatten the page
            servoGlass.glide_position(servoGlass.initial_position, speed=10)
            # 4. Scan the page
            # TODO
            time.sleep(1)
            # 5. Bring the glass up
            servoGlass.glide_position(0, speed=10)
            # 6. Grab the next page
            servoTurnerMain.glide_position(servoTurnerMain.initial_position, speed=5)
            servoTurnerSecondary.glide_position(
                servoTurnerSecondary.initial_position, speed=5
            )
            print(f"Finished page {i}")
            time.sleep(0.2)
    finally:
        servo_manager.arduino.close()
