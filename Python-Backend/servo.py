import time


class Servo:
    def __init__(self, id, servo_manager, initial_position):
        self.id = id
        self.servo_manager = servo_manager
        self.initial_position = initial_position
        self.set_position(initial_position)

    def set_position(self, target, wait=True):
        self.servo_manager.set_position(self.id, target)
        if wait:
            while self.servo_manager.get_position(self.id) != target:
                time.sleep(0.05)

    def glide_position(self, target, speed=1):
        current_position = self.get_position()
        step = 1 if target > current_position else -1

        while current_position != target:
            # Calculate next position step towards target
            if abs(target - current_position) < abs(step):
                # If the remaining distance is less than a step, go directly to the target
                next_position = target
            else:
                # Otherwise, move a step towards the target
                next_position = current_position + step

            self.set_position(next_position, wait=False)
            time.sleep(0.05 / speed)
            current_position = next_position

    def get_position(self):
        return self.servo_manager.get_position(self.id)


class InvertedServo(Servo):
    def set_position(self, target, wait=True):
        target = 180 - target
        super().set_position(target, wait)

    def glide_position(self, target, speed=1):
        target = 180 - target
        super().glide_position(target, speed)

    def get_position(self):
        return 180 - super().get_position()
