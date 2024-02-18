import time
from motor import Motor


class JoinedMotor(Motor):
    def __init__(self, motors):
        self.motors = motors

    def set_speed(self, target):
        for servo in self.servos:
            servo.set_speed(target, wait=False)

    def move_for(self, seconds, speed):
        for motor in self.motors:
            motor.set_speed(speed)
        time.sleep(seconds)
        for motor in self.motors:
            motor.set_speed(0)
        time.sleep(0.1)
