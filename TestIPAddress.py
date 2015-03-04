__author__ = 'omarsubhiabdelhafith'

import unittest
from IPAddress import IPAddress


class TestIPAddress(unittest.TestCase):

    def test_cidr(self):
        # When
        ip = "1.1.1.1"
        # Then
        assert IPAddress(ip).is_cidr() is False

        # When
        ip = "1.1.1.1/24"
        # Then
        assert IPAddress(ip).is_cidr() is True

    def test_parsed_id(self):
        # When
        ip = "1.1.1.1"
        # Then
        assert IPAddress(ip).parsed_ip == "1.1.1.1"
        assert IPAddress(ip).network == 32

        # When
        ip = "1.1.0.1"
        # Then
        assert IPAddress(ip).parsed_ip == "1.1.0.1"
        assert IPAddress(ip).network == 32

        # When
        ip = "1.1.1"
        # Then
        assert IPAddress(ip).parsed_ip == "1.1.1.0"
        assert IPAddress(ip).network == 32

        # When
        ip = "1.1"
        # Then
        assert IPAddress(ip).parsed_ip == "1.1.0.0"
        assert IPAddress(ip).network == 32

        # When
        ip = "1.1.1.1/24"
        # Then
        assert IPAddress(ip).parsed_ip == "1.1.1.1"
        assert IPAddress(ip).network == 24

        # When
        ip = "1.125.1/8"
        # Then
        assert IPAddress(ip).parsed_ip == "1.125.1.0"
        assert IPAddress(ip).network == 8

    def test_parsed_ip_validation(self):
        # When
        ip = "1.1.270.1"
        # Then
        self.assertRaises(TypeError, lambda: IPAddress(ip))

        # When
        ip = "1.900.270.1"
        # Then
        self.assertRaises(TypeError, lambda: IPAddress(ip))

        # When
        ip = "1.1.1.1/2000"
        # Then
        self.assertRaises(TypeError, lambda: IPAddress(ip))

        # When
        ip = "1.1.1.1/-2000"
        # Then
        self.assertRaises(TypeError, lambda: IPAddress(ip))

        # When
        ip = "1.1.1.1/xxxx"
        # Then
        self.assertRaises(ValueError, lambda: IPAddress(ip))

        # When
        ip = "1.1.1.1///"
        # Then
        self.assertRaises(ValueError, lambda: IPAddress(ip))

    def test_network_equality(self):
        # When
        ip = IPAddress("1.1.1.1")
        # Then
        assert ip.is_on_network("1.1/16") is True

        # When
        ip = IPAddress("1.2.3.4")
        # Then
        assert ip.is_on_network("1.1/16") is False

        # When
        ip = IPAddress("1.2.3.4")
        # Then
        assert ip.is_on_network("1.2.3/24") is True

        # When
        ip = IPAddress("1.2.3.4")
        # Then
        assert ip.is_on_network("1.2.3.4/32") is True

        # When
        ip = IPAddress("1.2.3.4")
        # Then
        assert ip.is_on_network("1.2.3.4/16") is True

        # When
        ip = IPAddress("1.2.3.4")
        # Then
        assert ip.is_on_network("1.2.60.70/16") is True

def main():
    unittest.main()

if __name__ == '__main__':
    main()