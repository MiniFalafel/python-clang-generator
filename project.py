#!/bin/python3

from config_object import ConfObj
from util import FormattedDocument

class ProjectConfig(ConfObj):
    def __init__(self, project: dict):
        super().__init__(project, "Project")
    
    ### FLAG GENERATION
    # INCLUDES
    def get_include_paths(self) -> list[str]:
        ### Gets include directories and evaluates tokens to compute paths
        includes = self.get_property("includeDirs", [])
        
        paths = []
        # de-tokenize each path
        for path in includes:
            paths.append("-I {}".format(path))
        # return
        return paths
    
    def get_include_flags(self) -> str:
        return " ".join(self.get_include_paths())
        
        
    # All flags
    def get_inline_flags(self):
        # TODO: make this actually parse include directories, linking directories, etc.
        include = self.get_include_flags()
        return include
    
    
    ### CLANGD GENERATION    
    def get_compile_flags(self) -> str:
        # Create a formatted document to build compile flags
        doc = FormattedDocument()
        
        # ConfigFlags header
        doc.push("CompileFlags:")
        
        # Write inline compile flags for "Add:"
        doc.write("Add: " + self.get_inline_flags())
        
        # Unindent
        doc.pop()
        
        return doc.read()
        
