__author__ = 'omarsubhiabdelhafith'

import json
import os
from IPAddress import IPAddress

""" IPAddressStorage
    This class is responsible for storing and loading a list of IPAddress from the storage
    It converts the IPAddress object to json, concatenate them, and store them on disk
"""
class IPAddressStorage(object):

    # Creates an IPAddressStorage that points to the storage_file file
    def __init__(self, storage_file):
        self.storage_file = storage_file
        self.storage_array = self.load_all()

    # Store the ip_address_obj to desk as a json object
    def store(self, ip_address_obj):
        arr = self.load_all()
        arr.append(ip_address_obj)

        json_array = map(lambda obj: obj.__dict__, arr)
        json.dump(json_array, open(self.storage_file, 'w'))

    # Load the json array from disk
    def load_all(self):
        try:
            items = json.load(open(self.storage_file))
            return map(lambda item: IPAddress.from_dict(**item), items)
        except IOError:
            return []

    # Clear storage
    def delete_storage(self):
        try:
            os.remove(self.storage_file)
        except OSError:
            pass






