import time
import numpy as np
from servo import Servo


class JoinedServo(Servo):
    def __init__(self, servos):
        self.servos = servos
        self.initial_position = self.servos[0].initial_position

    def set_position(self, target, wait=True):
        for servo in self.servos:
            servo.set_position(target, wait=False)
        if wait:
            for servo in self.servos:
                while servo.get_position() != target:
                    time.sleep(0.05)

    def glide_position(self, target, speed=1):
        current_positions = np.array([servo.get_position() for servo in self.servos])
        next_positions = np.zeros(len(self.servos))
        while not np.all(current_positions == target):
            # Calculate next position step towards target
            for i, current_position in enumerate(current_positions):
                step = 1 if target > current_position else -1
                if abs(target - current_position) < abs(step):
                    # If the remaining distance is less than a step, go directly to the target
                    next_position = target
                else:
                    # Otherwise, move a step towards the target
                    next_position = current_position + step
                next_positions[i] = next_position

            for i, servo in enumerate(self.servos):
                servo.set_position(next_positions[i], wait=False)
            time.sleep(0.05 / speed)
            current_positions = next_positions

    def get_position(self):
        return self.servos[0].get_position()
