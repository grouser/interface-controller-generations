import unittest
from coin_reader.controller import MControllerI


class MControllerITest(unittest.TestCase):
    def setUp(self):
        self.m_controlleri = MControllerI()

    def test_create_mcontrolleri_test(self):
        self.m_controlleri.device = None
        self.assertIsNotNone(self.m_controlleri.port)
        self.assertIsNotNone(self.m_controlleri.baud)
        self.assertIsNotNone(self.m_controlleri.timeout)
        self.assertIsNotNone(self.m_controlleri.parity)
        self.assertIsNotNone(self.m_controlleri.stopbits)
        self.assertIsNotNone(self.m_controlleri.bytesize)
        self.assertFalse(self.m_controlleri.coins_enabled)
        self.assertIsNone(self.m_controlleri.device)

    def test_connect_to_device(self):
        self.m_controlleri.connect_to_device()
        self.assertIsNotNone(self.m_controlleri.device)

    def test_open_connection(self):
        self.m_controlleri.connect_to_device()
        self.m_controlleri.open()
        self.assertTrue(self.m_controlleri.device.isOpen())
    
    def test_close_connection(self):
        self.m_controlleri.connect_to_device()
        self.m_controlleri.close()
        self.assertFalse(self.m_controlleri.device.isOpen())
    
    def test_send_message(self):
        self.assertEqual(self.m_controlleri.send_message("@"), 1)

    def test_enable_coins(self):
        self.m_controlleri.connect_to_device()
        self.m_controlleri.enable_coins()
        self.assertTrue(self.m_controlleri.coins_enabled)

    def test_disable_coins(self):
        self.m_controlleri.connect_to_device()
        self.m_controlleri.disable_coins()
        self.assertFalse(self.m_controlleri.coins_enabled)

    def test_enable_coins_reader_if_disabled(self):
        self.m_controlleri.connect_to_device()
        self.m_controlleri.disable_coins()
        self.m_controlleri.enable_coins_reader_if_disabled()
        self.assertTrue(self.m_controlleri.coins_enabled)

    def test_search_coin(self):
        self.assertEqual(self.m_controlleri._search_coin("Coin#1"), 0.05)
        self.assertEqual(self.m_controlleri._search_coin("Coin#2"), 2.00)
        self.assertEqual(self.m_controlleri._search_coin("Coin#3"), 0.10)
        self.assertEqual(self.m_controlleri._search_coin("Coin#4"), 0.20)
        self.assertEqual(self.m_controlleri._search_coin("Coin#5"), 0.50)
        self.assertEqual(self.m_controlleri._search_coin("Coin#6"), 1.00)
    
if __name__ == '__main__':
    unittest.main() 
