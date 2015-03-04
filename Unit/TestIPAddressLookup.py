__author__ = 'omarsubhiabdelhafith'

import unittest
from IPAddressLookup import *
from IPAddressStorage import *


class TestIPAddressLookup(unittest.TestCase):

    def setUp(self):
        self.storage = IPAddressStorage("ip_addresses_test")

    def test_can_lookup_ip_by_ip_address(self):
        # When
        self.storage.store(IPAddress("1.1.1.1"))
        self.storage.store(IPAddress("1.1.1.2"))
        self.storage.store(IPAddress("1.1.1.3"))

        # Then
        lookup = IPAddressLookup(self.storage)

        # expect
        assert lookup.find_ip_address(IPAddress("1.1.1.1")) is True

        # expect
        assert lookup.find_ip_address(IPAddress("2.1.1.1")) is False

    def test_can_lookup_ip_by_string(self):
        # When
        self.storage.store(IPAddress("1.1.1.1"))
        self.storage.store(IPAddress("1.1.1.2"))
        self.storage.store(IPAddress("1.1.1.3"))

        # Then
        lookup = IPAddressLookup(self.storage)

        # expect
        assert lookup.find_ip_address("1.1.1.1") is True

        # expect
        assert lookup.find_ip_address("2.1.1.1") is False

        # expect
        assert lookup.find_ip_address(IPAddress("2.1.1.1")) is False

        # expect
        assert lookup.find_ip_address(IPAddress("1.1.1.1")) is True

    def test_search_for_note(self):
        # When
        self.storage.store(IPAddress("1.1.1.1", "some note"))
        self.storage.store(IPAddress("1.1.1.2", "another note!"))
        self.storage.store(IPAddress("1.1.1.3", "and something else"))

        lookup = IPAddressLookup(self.storage)

        # Then
        assert len(lookup.search_for_note("some")) == 2
        assert len(lookup.search_for_note("another")) == 1
        assert len(lookup.search_for_note("note")) == 2

    def test_search_for_ip(self):
        # When
        self.storage.store(IPAddress("1.1.1.1", "some note"))
        self.storage.store(IPAddress("1.1.1.2", "another note!"))
        self.storage.store(IPAddress("1.1.1.3", "and something else"))

        lookup = IPAddressLookup(self.storage)

        # Then
        assert len(lookup.search_for_ip("1.1")) == 3
        assert len(lookup.search_for_ip("1.1.1")) == 3
        assert len(lookup.search_for_ip("1.1.2")) == 1
        assert len(lookup.search_for_ip("1..*3")) == 1
        assert len(lookup.search_for_ip("1.*2")) == 1

    def test_search_by_network(self):
        # When
        self.storage.store(IPAddress("1.2.3.4", "some note"))
        self.storage.store(IPAddress("1.2.10.20", "another note!"))
        self.storage.store(IPAddress("1.2.10.30", "and something else"))
        self.storage.store(IPAddress("1.22.10.30", "and something else"))
        self.storage.store(IPAddress("1.0.0.1", "and something else"))
        self.storage.store(IPAddress("1.0.0.1/8", "and something else"))

        lookup = IPAddressLookup(self.storage)

        # /8
        assert len(lookup.search_for_ip_cidr("1/8")) == 6
        assert len(lookup.search_for_ip_cidr("1.2.3.4/8")) == 6

        # /16
        assert len(lookup.search_for_ip_cidr("1/16")) == 2
        assert len(lookup.search_for_ip_cidr("1.2/16")) == 3
        assert len(lookup.search_for_ip_cidr("1.22/16")) == 1

        # /24
        assert len(lookup.search_for_ip_cidr("1/24")) == 2
        assert len(lookup.search_for_ip_cidr("1.0/24")) == 2
        assert len(lookup.search_for_ip_cidr("1.0.0/24")) == 2
        assert len(lookup.search_for_ip_cidr("1.2.10/24")) == 2
        assert len(lookup.search_for_ip_cidr("1.22.10/24")) == 1

        # /32
        assert len(lookup.search_for_ip_cidr("1.2.3.4/32")) == 1
        assert len(lookup.search_for_ip_cidr("1.22.10.30/32")) == 1
        assert len(lookup.search_for_ip_cidr("1/32")) == 0

    def tearDown(self):
        self.storage.delete_storage()


def main():
    unittest.main()

if __name__ == '__main__':
    main()