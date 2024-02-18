from servo_manager import ServoManager
from servo import Servo
from motor import Motor, InvertedMotor
from joined_motor import JoinedMotor
import time
import itertools

UP_TIME = 3
DOWN_TIME = 2


def calibrate_glass(motor: Motor):
    while input("Glass is up. (y/n) ") != "y":
        motor.move_for(1, -motor.operating_speed)


def calibrate_turner(servoTurnerMain: Servo, servoTurnerSecondary: Servo):
    while True:
        command = input(
            "Move turner main arm (m,amount), secondary arm (s,amount), or done (d) "
        )
        if command == "d":
            break
        if "," not in command:
            print("Invalid command")
            continue
        command, amountRaw = command.split(",")
        if not amountRaw.strip("-").isnumeric():
            print("Invalid amount")
            continue
        amount = int(amountRaw)
        if command == "m":
            servoTurnerMain.glide_position(
                max(0, min(180, servoTurnerMain.get_position() + amount)), speed=5
            )
        elif command == "s":
            servoTurnerSecondary.glide_position(
                max(0, min(180, servoTurnerSecondary.get_position() - amount)),
                speed=5,
            )


def control(callback):
    servo_manager = ServoManager()
    print("Connected to Arduino")
    servoTurnerMain = Servo(0, servo_manager, 160)
    servoTurnerSecondary = Servo(1, servo_manager, 180)
    print("Servos initialized")
    motorGlassLeft = Motor(2, servo_manager)
    motorGlassRight = Motor(3, servo_manager)
    try:
        motorGlass = JoinedMotor(
            [motorGlassLeft, motorGlassRight]
        )  # - is up, + is down
        motorGlass.operating_speed = 255

        print("Calibrating glass")
        calibrate_glass(motorGlass)

        servoTurnerSecondary.glide_position(10, speed=5)

        print("Calibrating turner")
        calibrate_turner(servoTurnerMain, servoTurnerSecondary)
        servoTurnerMain.initial_position = servoTurnerMain.get_position()
        servoTurnerSecondary.initial_position = servoTurnerSecondary.get_position()

        print("Calibration finished")

        for i in itertools.count():
            print(f"Starting page {i}")
            # 1. Turn the page
            servoTurnerMain.glide_position(50, speed=3)
            # 2. Release the page
            servoTurnerSecondary.glide_position(120, speed=3)
            time.sleep(0.5)  # Wait for the page to fall
            # servoTurnerSecondary.glide_position(30, speed=5)
            # 4. Bring the glass down to flatten the page
            motorGlass.move_for(DOWN_TIME, motorGlass.operating_speed)
            # 3. Move above the glass to get ready for reset
            servoTurnerMain.glide_position(160, speed=5)
            servoTurnerSecondary.glide_position(120, speed=5)
            # 5. Scan the page
            callback()
            print(f"Scanned page {i}")
            # 6. Bring the glass up
            motorGlass.move_for(UP_TIME, -motorGlass.operating_speed)
            # 7. Grab the next page
            servoTurnerMain.glide_position(servoTurnerMain.initial_position, speed=5)
            servoTurnerSecondary.glide_position(
                servoTurnerSecondary.initial_position, speed=5
            )
            print(f"Finished page {i}")
            time.sleep(0.5)
    finally:
        motorGlassLeft.set_speed(0)
        motorGlassRight.set_speed(0)
        servo_manager.arduino.close()
