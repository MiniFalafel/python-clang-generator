#!/bin/python3

from config_object import ConfObj
from util import FormattedDocument

class ProjectConfig(ConfObj):
    def __init__(self, project: dict):
        super().__init__(project, "Project")
        
    # Path property getters
    
    def __gen_path(self, path, tokens: dict) -> str:
        # Try replacing each token with the value from the dict
        for token, value in tokens.items():
            path = path.replace(token, value)
        # Return
        return path
    
    def get_location(self, tokens: dict) -> str:
        ### Returns the "location" property as a path
        location = self.__gen_path(self.get_property("location"), tokens)
        return location
    
    
    ### FLAG GENERATION
    
    # INCLUDES
    def get_include_paths(self, tokens: dict) -> list[str]:
        ### Gets include directories and evaluates tokens to compute paths
        includes = self.get_property("includeDirs", [])
        
        paths = []
        # de-tokenize each path
        for path in includes:
            paths.append("-I {}".format(self.__gen_path(path, tokens)))
        # return
        return paths
    
    def get_include_flags(self, tokens: dict) -> str:
        return " ".join(self.get_include_paths(tokens))
        
        
    # All flags
    def get_inline_flags(self, tokens: dict):
        # TODO: make this actually parse include directories, linking directories, etc.
        include = self.get_include_flags(tokens)
        return include
    
    
    ### CLANGD GENERATION    
    def get_compile_flags(self, tokens: dict) -> str:
        # Create a formatted document to build compile flags
        doc = FormattedDocument()
        
        # ConfigFlags header
        doc.push("CompileFlags:")
        
        # Write inline compile flags for "Add:"
        doc.write("Add: " + self.get_inline_flags(tokens))
        
        # Unindent
        doc.pop()
        
        return doc.read()
        
