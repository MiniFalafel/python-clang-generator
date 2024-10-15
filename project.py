#!/bin/python3

from config_object import ConfObj
from util import FormattedDocument, get_os_command, detokenize
from stat_paths import Paths

class ProjectConfig(ConfObj):
    def __init__(self, project: dict, name: str):
        super().__init__(project, name, "Project")
        
        # Setup location
        self.location = None
        self.get_location()
    
    # PUBLIC GETTERS
    def get_location(self):
        if self.location is not None:
            return self.location
        ### Gets project location as relative path
        self.location = self.get_property("location")
        # Detokenize
        self.location = detokenize(self.location)
        
        # return
        return self.location
    
    def get_files(self):
        ### Gets the "files" property and evaluates them as actual paths
        files = self.get_property("files")
        # evaluate the paths using os terminal
        evaluated_paths = []
        loc = self.get_location()
        for path in files:
            p = "{}/{}".format(loc, path)
            evaluated_paths.append(get_os_command("find . -path {}".format(p, str(Paths.MAX_DEPTH))))
        # join the filepaths into a single string
        files = " ".join(evaluated_paths)
        # detokenize the file paths
        files = detokenize(files, self.location)
        return files
    
    # Property getters
    def get_bin_dir(self):
        bin_dir = self.get_property("bin", "bin")
        return detokenize(bin_dir, self.location)
    
    def __get_output_name(self):
        return "{}/{}".format(self.get_bin_dir(), self.name)
    
    # applies format to all elements of list and concatenates them.
    def __format_list(self, format_template: str, _list: list):
        return "".join([format_template.format(el) for el in _list])
    
    # include directories
    def __get_include_flags(self):
        includes = self.get_property("includeDirs")
        # detokenize the include dirs
        detok_includes = []
        for path in includes:
            detok_includes.append(detokenize(path, self.location))
        # return formatted as inline
        return self.__format_list(" -I {}", detok_includes)
    
    # get link dirs
    def __get_link_flags(self):
        # Get link names
        links = self.get_property("links")
        # If nothing was gotten, don't try and link'
        if links is None:
            return ""
        
        # Add other project binary directories to link paths
        # NOTE: We can do this every time because link paths don't add the link names themselves
        link_paths = []
        for k, v in Paths.BIN_PATHS.items():
            # Don't add self bin path
            if k == self.name:
                continue
            # These paths are already detokenized, add them to link path directly
            link_paths.append(v)
        
        # Convert to flags and return
        link_dirs = self.__format_list(" -L {}", link_paths)
        link_files = self.__format_list(" -l{}", links)
        
        # return both next to each other
        return "{} {}".format(link_dirs, links)
        
    
    ### Build command generation
    def gen_build_command(self) -> str:
        props = {
            "compiler" : self.get_property("compiler", "clang++"),
            "flags" : "--std={}".format(self.get_property("cpp", "c++17")),
            "files" : self.get_files(),
            "output" : self.__get_output_name(),
            "includes" : self.__get_include_flags(),
            "linking" : self.__get_link_flags()
        }
        # format string
        r = "{compiler} {flags} {files} -o {output} {includes} {linking}".format(**props)
        r = r.replace("\n", " ")
        
        return r
    
    def write_build_file(self):
        # Get the build command
        command = self.gen_build_command()
        # Create build script file
        f = open("{}/clang_build.sh".format(self.location), "w")
        # Write
        f.write("{}\n".format(command))
        # close file
        f.close()
    
    ### CLANGD GENERATION    
    def get_clangd(self) -> str:
        # Create a formatted document to build compile flags
        doc = FormattedDocument()
        
        # ConfigFlags header
        doc.push("CompileFlags:")
        
        # Write inline compile flags for "Add:"
        #doc.write("Add: " + self.get_inline_flags())
        
        # Unindent
        doc.pop()
        
        return doc.read()
        
