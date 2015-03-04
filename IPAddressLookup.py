__author__ = 'omarsubhiabdelhafith'

import re
from IPAddress import *

""" IPAddressLookup
    IPAddressLookup is responsible for the lookup of ip address from disk
    It access the persistence layer through IPAddressStorage
"""
class IPAddressLookup(object):

    # Creates a IPAddressLookup that owns a IPAddressStorage
    def __init__(self, ip_address_storage):
        self.ip_address_storage = ip_address_storage

    # Searches for an ip address in the storage.
    # ip_address can either be of type String or IPAddress
    def find_ip_address(self, ip_address):
        all_ips = self.ip_address_storage.load_all()

        if ip_address.__class__ == IPAddress:
            return ip_address in all_ips
        else:
            return IPAddress(ip_address) in all_ips

    # Searches for an ip address or part of it
    # For example, passing 1.1 will match 1.1.1.1, 1.2.1.1, 3.1.1.5
    def search_for_ip(self, expression):
        items = self.ip_address_storage.load_all()
        return filter(lambda item: IPAddressLookup.matches_ip(item, expression), items)

    # Searches all the ip addresses that are on the same CIDR network
    # Example:
    # Passing 1.1/16 will match 1.1.16.20, 1.1.20.0
    # Passing 2/16 will match 2.0.1.0, 2.0.20.30
    # Passing 2/24 will match 2.0.0.1, 2.0.0.25
    def search_for_ip_cidr(self, expression):
        items = self.ip_address_storage.load_all()
        return filter(lambda item: IPAddressLookup.matches_network(item, expression), items)

    # Searches for a note or part of it
    def search_for_note(self, expression):
        items = self.ip_address_storage.load_all()
        return filter(lambda item: IPAddressLookup.matches_note(item, expression), items)

    # Internal methods
    @staticmethod
    def matches_note(ip_address, exp):
        if not ip_address.note:
            return False

        exp = ".*%s.*" % exp
        return re.search(exp, ip_address.note)

    @staticmethod
    def matches_network(ip_address, exp):
        return ip_address.is_on_network(exp)

    @staticmethod
    def matches_ip(ip_address, exp):
        exp = ".*%s.*" % exp
        return re.search(exp, ip_address.parsed_ip)


