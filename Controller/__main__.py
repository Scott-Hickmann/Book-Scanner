from servo_manager import ServoManager
from servo import Servo, InvertedServo
from joined_servo import JoinedServo
import time
import itertools

INITIAL_TURNER_MAIN_POSITION = 90
INITIAL_TURNER_SECONDARY_POSITION = 180


def calibrate_glass(servo: Servo, initial_position):
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
                servoTurnerMain.get_position() - amount, speed=5
            )
        elif command == "s":
            servoTurnerSecondary.glide_position(
                servoTurnerSecondary.get_position() - amount,
                speed=5,
            )


if __name__ == "__main__":
    try:
        servo_manager = ServoManager()
        servoTurnerMain = Servo(0, servo_manager, INITIAL_TURNER_MAIN_POSITION)
        servoTurnerSecondary = Servo(
            1, servo_manager, INITIAL_TURNER_SECONDARY_POSITION
        )
        servoGlassLeft = Servo(2, servo_manager, 0)
        servoGlassRight = InvertedServo(3, servo_manager, 0)
        servoGlass = JoinedServo([servoGlassLeft, servoGlassRight])

        servoTurnerMain.glide_position(20, speed=5)  # So that the glass doesn't hit it

        print("Calibrating glass")
        calibrate_glass(servoGlass, 0)
        servoGlass.initial_position = servoGlass.get_position()

        servoGlass.glide_position(
            0, speed=5
        )  # Bring the glass back up to avoid hitting the turner
        servoTurnerMain.glide_position(
            INITIAL_TURNER_MAIN_POSITION, speed=5
        )  # Bring the turner back to its initial position
        servoTurnerSecondary.glide_position(INITIAL_TURNER_SECONDARY_POSITION, speed=5)

        print("Calibrating turner")
        calibrate_turner(servoTurnerMain, servoTurnerSecondary)
        servoTurnerMain.initial_position = servoTurnerMain.get_position()
        servoTurnerSecondary.initial_position = servoTurnerSecondary.get_position()

        print("Calibration finished")

        for i in itertools.count():
            print(f"Starting page {i}")
            # 1. Turn the page
            servoTurnerMain.glide_position(100, speed=3)
            # 2. Release the page
            servoTurnerSecondary.glide_position(120, speed=5)
            # 3. Move out of the way for the glass
            servoTurnerMain.glide_position(servoTurnerMain.initial_position, speed=5)
            # 4. Bring the glass down to flatten the page
            servoGlass.glide_position(servoGlass.initial_position, speed=10)
            # 5. Scan the page
            # TODO
            time.sleep(1)
            # 6. Bring the glass up
            servoGlass.glide_position(0, speed=10)
            # 7. Grab the next page
            servoTurnerSecondary.glide_position(
                servoTurnerSecondary.initial_position, speed=5
            )
            print(f"Finished page {i}")
            time.sleep(0.2)
    finally:
        servo_manager.arduino.close()
