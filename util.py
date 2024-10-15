#!/bin/bash

import os
import subprocess

from stat_paths import Paths

# ------------------------------------------- #
##=> MISCELLANEOUS
# ------------------------------------------- #

def get_os_command(command: str):
    # Get split command
    split_comm = command.split(" ")
    
    # Give split_comm to subprocess
    result = subprocess.run(split_comm, stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8')[:-1] # Slice off newline at the end


def get_pwd():
    return get_os_command("pwd")

# ------------------------------------------- #
##=> ERROR LOGGING
# ------------------------------------------- #
class ERROR:
    # Static variables
    NONE = ""
    ERROR = "ERROR"
    WARN = "WARNING"
    
    PARSING = "PARSING_ERROR"
    FILE = "FILE_ERROR"
    
    FORMAT = "FORMATTING_ERROR"

def log_err(msg: str, err_type: ERROR = ERROR.NONE, should_abort: bool = True):
    print("{}: {}".format(err_type, msg))
    if should_abort:
        print("Aborting...")
        exit(1)
        
    
# ------------------------------------------- #
##=> FILE + STRING UTILS
# ------------------------------------------- #

class FormattedDocument:
    def __init__(self, base_indent: int = 0):
        self.indent = base_indent
        
        self.line_buffer = []
        
    def write(self, line: str):
        tabs = "    " * self.indent
        self.line_buffer.append(tabs + line)
        
    def push(self, push_char: str = ""):
        # Write opening char
        self.write(push_char)
        # Then indent
        self.indent += 1
        
    def pop(self, pop_char: str = ""):
        # Unindent first
        self.indent -= 1
        # Check that we didn't pop disproportionately
        if self.indent < 0:
            log_err("Can't unindent on pop", ERROR.FORMAT)
        # Now write closing token
        self.write(pop_char)
        
    def read(self):
        return "\n".join(self.line_buffer)
        
        
# Token removal
def detokenize(string: str, proj_location: str = ""):
    """ string: the string you want to detokenize.
        tokens: dictionary - keys are the tokens, values are what they should be replaced with
    """
    tokens = Paths.PATHS.copy()
    tokens["PRJ_DIR"] = proj_location
    for k, v in tokens.items():
        string = string.replace("%{*}".replace("*", k), v)
    return string
