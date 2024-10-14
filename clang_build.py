#!/bin/python3

### ===> THIS IS THE DRIVER FILE <===
### This handles user input and runs correct code based on arguments

import sys

from generate import gen_driver

# ENTRY POINT
if __name__ == "__main__":
    # argument and option parsing
    options = []    # array of tuples. if an option takes an argument, this will be something like ("-opt", "arg"), - if not, ("-o"),
    arguments = []  # array of all other arguments
    
    # Loop through sys.argv
    for arg in sys.argv:
        # Check if it's an option'
        if arg.startswith("-"):
            # Split the option apart where it has an "=" (i.e. where arg was specified)
            op_list = tuple(arg.split("="))
            # If there was more than one "=", there shouldn't be
            if len(op_list) > 2:
                print("Options can only take one argument value, user specified too many: '{}'".format(str(op_list)))
                exit(1)
            # Append
            options.append(op_list)
        else:
            # This was an argument
            arguments.append(arg)
            
    print("OPTIONS: {}\nARGS: {}".format(str(options), str(arguments)))
            
    # Pass args and options to generate function
    gen_driver(arguments, options)
