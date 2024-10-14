#!/bin/python3

from util import log_err, ERROR


class ConfObj:
    def __init__(self, conf_dict: dict, type_name: str):
        self.conf = conf_dict
        self.name = type_name
        
    def get_property(self, prop_name: str, default_val = None):
        prop = default_val
        # Try getting the property
        try:
            prop = self.conf[prop_name]
        except KeyError:
            log_err("{} property '{}' not specified, defaulting to '{}'".format(self.name, prop_name, default_val), ERROR.WARN, False)
        # return
        return prop
