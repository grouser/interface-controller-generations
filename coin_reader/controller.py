import re
import serial


COINS_CODE = {
    'Coin#1': '0.05',
    'Coin#2': '2.00',
    'Coin#3': '0.10',
    'Coin#4': '0.20',
    'Coin#5': '0.50',
    'Coin#6': '1.00',
}


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
        self.coins_enabled = False # Controller doesn't read any coin by default
        self.connect_to_device()

    def connect_to_device(self):
        try:
            self.device = serial.Serial(self.port, self.baud, timeout=self.timeout,
                                        parity=self.parity, stopbits=self.stopbits,
                                        bytesize=self.bytesize)
        except serial.SerialException as exp:
            print "Error: Device doesn't exist or can not be configured. Output: {}".format(exp)
        except serial.ValueError as exp:
            print "Some values are out of range. Output: {}".format(exp)
            self.device = None

    def open(self):
        """Start connection with the device"""
        if not self.device.isOpen():
            self.device.open()

    def close(self):
        """Close the connection with the device"""
        if self.device.isOpen():
            self.device.close()

    def send_message(self, message):
        return self.device.write(message)

    def _search_coin(self, coin):
        """Detects if a coin is inserted"""
        try:
            amount = COINS_CODE[str(coin)]
            return float(amount)
        except Exception as e:
            print e

    def listen_for_coins(self):
        """Listen any message until Control + C is pressed"""
        self.enable_coins_reader_if_disabled()
        coin_regex = re.compile("Coin#[1-6]")
        while True:
            msg = self.device.readall()
            match = coin_regex.search(msg)
            if match:
                try:
                    print self._search_coin(match.group(0))
                except Exception as e:
                    print e

    def listen_any_message(self):
        self.enable_coins_reader_if_disabled()
        while True:
            msg = self.device.readall()
            print msg

    def enable_coins(self):
        """Enables the reader to read coins"""
        self.device.write("@")
        self.coins_enabled = True

    def disable_coins(self):
        """Disables the reader to read coins"""
        self.device.write("?")
        self.coins_enabled = False

    def enable_coins_reader_if_disabled(self):
       if not self.coins_enabled:
           self.enable_coins()
