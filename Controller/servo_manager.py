import serial
import serial.tools.list_ports
import time


def find_arduino_serial_port():
    """Attempt to auto-detect the serial port for the first Arduino connected."""
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if "usbmodem" in p.name:
            print(p.name)
            return p.device
    return None


def connect_to_arduino(port):
    """Connect to the specified serial port at 9600 baud rate."""
    try:
        arduino = serial.Serial(port, baudrate=9600, timeout=0.1)
        time.sleep(2)  # wait for the Arduino to reset
        return arduino
    except serial.SerialException:
        return None


class ServoManager:
    def __init__(self):
        port = find_arduino_serial_port()
        if port is None:
            raise Exception("Arduino not found. Please ensure it is connected.")
        print(f"Found Arduino on port {port}")
        self.arduino = connect_to_arduino(port)
        if not self.arduino:
            raise Exception(f"Failed to connect to Arduino on {port}")

    def set_position(self, servo_id, position):
        print(f"Setting servo {servo_id} to position {position}")
        data = f"{servo_id},{position}\n"
        self.arduino.write(data.encode("utf-8"))
        # time.sleep(0.5)
        # self.arduino.write(f"h".encode("utf-8"))
        # time.sleep(1)
        # data = self.arduino.readline()
        # time.sleep(0.1)
        # print(data)
        # data = self.arduino.readline()
        # time.sleep(0.1)
        # print(data)
