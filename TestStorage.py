__author__ = 'omarsubhiabdelhafith'

import unittest
from IPAddressStorage import *
from IPAddress import  *

class TestStorage(unittest.TestCase):

    def setUp(self):
        self.subject = IPAddressStorage("ip_addresses_test")

    def test_can_save_ip(self):
        # When
        ip = IPAddress("1.2.1.1")
        self.subject.store(ip)
        # Then
        assert IPAddress("1.2.1.1") in self.subject.load_all()

        # When
        ip = IPAddress("1.2.2.1")
        self.subject.store(ip)
        # Then
        assert IPAddress("1.2.1.1") in self.subject.load_all()
        assert IPAddress("1.2.2.1") in self.subject.load_all()

    def test_can_store_note(self):
        # When
        ip = IPAddress("1.2.1.1")
        ip.note = "Hello Everyone"
        self.subject.store(ip)
        # Then
        assert self.subject.load_all()[0].note == "Hello Everyone"

        # When
        ip = IPAddress("1.2.4.1")
        ip.note = {"1": "2"}
        self.subject.store(ip)
        # Then
        assert self.subject.load_all()[1].note == {"1": "2"}

    def tearDown(self):
        self.subject.delete_storage()


def main():
    unittest.main()

if __name__ == '__main__':
    main()