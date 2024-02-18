import time


class Motor:
    def __init__(self, id, servo_manager):
        self.id = id
        self.servo_manager = servo_manager
        self.set_speed(0)

    def set_speed(self, target):
        self.servo_manager.set_position(self.id, target)

    def move_for(self, seconds, speed):
        self.set_speed(speed)
        time.sleep(seconds)
        self.set_speed(0)


class InvertedMotor(Motor):
    def set_speed(self, target):
        target = 180 - target
        super().set_speed(target)
