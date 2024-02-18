from servo_manager import ServoManager
from servo import Servo
from motor import Motor, InvertedMotor
from joined_motor import JoinedMotor
import time
import itertools


def calibrate_glass(servo: Servo):
    while True:
        command = input("Move glass (amount) or done (d) ")
        if command == "d":
            break
        if not command.strip("-").isnumeric():
            print("Invalid amount")
            continue
        amount = int(command)
        servo.glide_position(servo.get_position() + amount, speed=5)


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
                servoTurnerMain.get_position() + amount, speed=5
            )
        elif command == "s":
            servoTurnerSecondary.glide_position(
                servoTurnerSecondary.get_position() - amount,
                speed=5,
            )


if __name__ == "__main__":
    try:
        servo_manager = ServoManager()
        print("Connected to Arduino")
        servoTurnerMain = Servo(0, servo_manager, 160)
        servoTurnerSecondary = Servo(1, servo_manager, 180)
        print("Servos initialized")
        motorGlassLeft = Motor(2, servo_manager)
        motorGlassRight = InvertedMotor(3, servo_manager)
        motorGlass = JoinedMotor([motorGlassLeft, motorGlassRight])

        servoTurnerMain.glide_position(160, speed=5)  # So that the glass doesn't hit it

        print("Calibrating glass")
        # calibrate_glass(servoGlass)
        motorGlass.operating_speed = 120

        motorGlass.move_for(5, motorGlass.operating_speed)
        # Bring the glass back up to avoid hitting the turner
        servoTurnerSecondary.glide_position(180, speed=5)

        print("Calibrating turner")
        calibrate_turner(servoTurnerMain, servoTurnerSecondary)
        servoTurnerMain.initial_position = servoTurnerMain.get_position()
        servoTurnerSecondary.initial_position = servoTurnerSecondary.get_position()

        print("Calibration finished")

        for i in itertools.count():
            print(f"Starting page {i}")
            # 1. Turn the page
            servoTurnerMain.glide_position(80, speed=3)
            # 2. Release the page
            servoTurnerSecondary.glide_position(90, speed=5)
            time.sleep(0.5)  # Wait for the page to fall
            servoTurnerSecondary.glide_position(30, speed=5)
            # 3. Move out of the way for the glass
            servoTurnerMain.glide_position(servoTurnerMain.initial_position, speed=5)
            servoTurnerSecondary.glide_position(100, speed=5)
            # 4. Bring the glass down to flatten the page
            motorGlass.move_for(5, motorGlass.operating_speed)
            # 5. Scan the page
            # TODO
            time.sleep(1)
            # 6. Bring the glass up
            motorGlass.move_for(5, -motorGlass.operating_speed)
            # 7. Grab the next page
            servoTurnerSecondary.glide_position(
                servoTurnerSecondary.initial_position, speed=5
            )
            print(f"Finished page {i}")
            time.sleep(0.2)
    finally:
        servo_manager.arduino.close()
