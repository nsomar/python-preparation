__author__ = 'omarsubhiabdelhafith'
from binascii import *
from itertools import *

""" IPAddress
    IPAddress represents an IP address.
    Fields:
        - ip_components(readonly): the ip components (1.1.1.1) has [1,1,1,1] components
        - note(read, write): a note attached to the ip address
        - network(readonly): the CIDR network that this ip belongs to
"""
class IPAddress(object):

    # Creates an IPAddress from a string and a note, the passed string will be parsed and validated
    def __init__(self, string, note=None):
        self.ip_components = None
        self.__note = None
        self.raw_string = string
        self.network = 32
        self.note = note

        self.parse()
        self.validate()

        self.parsed_ip = ".".join([str(int_value) for int_value in self.ip_components])

    # Factory method to create an IPAddress from a dictionary
    @classmethod
    def from_dict(cls, **entries):
        ip = cls("")
        ip.__dict__.update(entries)
        return ip

    # Get the note value
    @property
    def note(self):
        return self.__note

    # Set the note value
    @note.setter
    def note(self, value):
        self.__note = value

    # Checks if the IPAddress belongs to a network
    # Example:
    #   - IPAddress of 1.2.3.4 belongs to networks 1/8, 1.100/8, 1.2/16, 1.2.3/24
    def is_on_network(self, network):
        ip = IPAddress(network)
        binary_mask = int(ip.cidr_mask(), 2)

        # Compare by bitwise and the mask and the ip
        binary_ip1 = int(self.binary_ip_string(), 2)
        binary_ip2 = int(ip.binary_ip_string(), 2)
        return (binary_ip1 & binary_mask) == (binary_ip2 & binary_mask)

    def cidr_mask(self):
        return ("1" * self.network) + ("0" * (32 - self.network))

    def binary_ip_string(self):
        return "".join(map(lambda x: '{0:08b}'.format(x), self.ip_components))

    # Internal methods
    def is_cidr(self):
        return "/" in self.raw_string

    def __eq__(self, other):
        return self.parsed_ip == other.parsed_ip and self.note == other.note

    def parse(self):
        if self.is_cidr():
            self.parse_cidr()
        else:
            self.parse_ip(self.raw_string)

    def parse_cidr(self):
        components, network = self.raw_string.split("/")
        self.network = int(network)
        self.parse_ip(components)

    def parse_ip(self, ip_address):
        components = ip_address.split(".")
        # fill with zeros
        while len(components) < 4:
            components.append("0")

        # remove empty gaps
        components = map(lambda value: value if value != "" else "0", components)
        # convert to ints
        components = map(lambda value: int(value), components)

        self.ip_components = components

    def validate(self):
        # check ip components
        for value in self.ip_components:
            if value > 255:
                raise TypeError("Invalid IP component {0} for ip {1}".format(value, self.raw_string))

        try:
            self.validate_network(self.network)
        except TypeError, e:
            raise TypeError(str(e) + " for ip {0}".format(self.raw_string))

    def validate_network(self, network):
        # check network
        if network > 32 or network < 0:
            raise TypeError("Network value of {0} is not correct".format(network))
