import time


class Servo:
    def __init__(self, servo_id, servo_manager, initial_position):
        self.servo_id = servo_id
        self.servo_manager = servo_manager
        self.initial_position = initial_position
        self.reset()

    def set_position(self, target):
        self.servo_manager.set_position(self.servo_id, target)
        while self.get_position() != target:
            time.sleep(0.05)
        self.position = target

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

            self.servo_manager.set_position(self.servo_id, next_position)
            time.sleep(0.05 / speed)
            current_position = next_position

    def get_position(self):
        return self.servo_manager.get_position(self.servo_id)

    def reset(self):
        self.set_position(self.initial_position)
