import serial


class MControllerI(object):
    """
    Implements functions to talk with a Multi-Function Controller
    Interface from Future Generations
    """
    def __init__(self, port="/dev/ttyUSB0", baud=9600, timeout=1,
                 parity=serial.PARITY_NONE, stopbits=1,
                 bytesize=serial.EIGHTBITS):
        self.port = port
        self.baud = baud
        self.timeout = timeout
        self.parity = parity
        self.stopbits = stopbits
        self.bytesize = bytesize

        self.device = serial.Serial(self.port, self.baud, self.timeout,
                                    self.parity, self.stopbits, self.bytesize)

    def open(self):
        """Start connection with the device"""
        if not self.device.isOpen():
            self.device.open()

    def close(self):
        """Close the connection with the device"""
        if self.device.isOpen():
            self.device.close()

    def send_message(self, message):
        self.device.write(message)

    def listen_any_message(self):
        """Listen any message until Control + C is pressed"""
        while True:
            self.device.readall()
