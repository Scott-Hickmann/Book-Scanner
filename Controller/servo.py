class Servo:
    def __init__(self, servo_id, servo_manager):
        self.servo_id = servo_id
        self.servo_manager = servo_manager
        self.set_position(0)

    def set_position(self, position):
        self.servo_manager.set_position(self.servo_id, position)
        self.position = position
