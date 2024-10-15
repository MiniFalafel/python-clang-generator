#!/bin/python3

import json

from util import FormattedDocument, get_pwd, detokenize
from stat_paths import Paths
from workspace import WorkspaceConfig


# ------------------------------------------- #
##=> PARSING 
# ------------------------------------------- #

def get_json_object(json_string: str):
    r = json.loads(json_string)
    if type(r) != dict:
        log_err("json provided is not object")
    return r

def generate_build_script(wks: WorkspaceConfig):
    ### GENERATES BUILD AND RUN SCRIPTS
    
    # For each project, generate build commands
    build_commands = []
    for proj in wks.get_projects():
        proj.write_build_file()
    
    print("TODO: Implement build script generation...")


def generate_clangd_files(wks: WorkspaceConfig):
    ### Generates ".clangd" files for both the workspace and all projects specified in workspace
    
    # Get workspace working directory
    wks_dir = wks.get_property("location")
    # Replace any "." with the pwd
    wks_dir = wks_dir.replace(".", get_pwd())
    
    # Get projects array
    projects = wks.get_property("projects")
    strings = []
    # Generate configurations for each project
    for proj_name in projects:
        # Try getting the project as an object from its name
        proj = wks.get_project(proj_name)
        # Get location property
        location = proj.get_property("location")
        location = detokenize(location)
        
        # Get project compile flags
        compile_flags = detokenize(proj.get_clangd(), location)
        strings.append(compile_flags)
    return strings

# Generate build script from json string
def generate_from_string(json_str: str):
    # Decode json parsed string to a WorkspaceConfig object
    workspace = WorkspaceConfig(get_json_object(json_str))
    
    # Get project binary directories and add them to Paths
    for proj in workspace.get_projects():
        Paths.BIN_PATHS[proj.name] = proj.get_bin_dir()
    
    # Generate the build script
    script = generate_build_script(workspace)
    
    # Generate ".clangd" files
    generate_clangd_files(workspace)
    
    # Output the script to console
    print(script)
    
def generate_from_file(filepath: str):
    # Try opening the file
    try:
        f = open(filepath)
        generate_from_string(f.read())
    except FileNotFoundError:
        log_err("No such file exists: '{}'".format(filepath), ERROR.FILE)
    except PermissionError:
        log_err("Permission denied: '{}'".format(filepath), ERROR.FILE)
        



# ------------------------------------------- #
##=> HELP, USAGE, ETC 
# ------------------------------------------- #
    
def get_example_config():
    example_config = """{
    "location" : "."
    "projects" : ["project 1", "project 2"],
    "start_proj" : "project 2",
    
    "project 1" : {
        "location" : "%{WKS_DIR}/proj1",
        "kind" : "static"
        
        "bin" : "%{PRJ_DIR}/bin",
        
        "files" : [
            "src/*.h",
            "src/*.cpp"
        ],
        
        "defines" : [
            "PROJ_1_DEFINE"
        ],
        
        "includeDirs" : [
            "%{PRJ_DIR}/src"
        ]
    },
    
    "project 2" : {
        "location" : "%{WKS_DIR}/proj2",
        "kind" : "console"
        
        "bin" : "%{PRJ_DIR}/bin",
        
        "files" : [
            "src/*"
        ],
        
        "includeDirs" : [
            "%{PRJ_DIR}/src",
            "%{WKS_DIR}/proj1/src"
        ],
        
        "links" : [
            "project 1"
        ]
    }
    \n}
    """
    return example_config


def help_example_config():
    help_str = """CONFIGURATION FILES:
    Config files should be written in json format. Here's a list of properties that the parser expects:

    WORKSPACE:
        > "location"     : string   ~ Specifies the working directory of the workspace, relative to pwd of generate script. Can be accessed with "%{WKS_DIR}" and will be interpreted by the parser
        > "projects"     : array    ~ The names of other properties which should parsed and configured as projects.
        > "startproject" : string   ~ Tells the workspace which project's binary should be run after compile.
        
    PROJECTS:
        Note that the names of the properties can be anything. As long as they're listed in the "projects" property for the workspace, they'll be generated.
        > "location"    : string   ~ Specifies the working directory of the project, from which other paths are derived (e.g. "files" property). Can be accessed with "%{PROJ_DIR}" and will be interpreted by the parser
        > "kind"        : string   ~ Specifies the type of binary to be compiled. Can be any of the following:
            *   "console", "staticlib", "sharedlib"
                -   "console"   : console app - directly executable.
                -   "staticlib" : static library - contains definitions of symbols for compile-time linking
                -   "sharedlib" : shared library - contains definitions of symbols for runtime linking
        > "bin"         : string   ~ Specifies the directory where binaries will be after compile
        > "files"       : array    ~ A list of which files the compiler should be looking for.
        > "defines"     : array    ~ A list of compiler definitions that should be used
        > "includeDirs" : array    ~ A list of directories which should be included by the compiler
        > "links"       : array    ~ A list of projects binaries and/or libraries that should be linked
    """
    
    # Add configuration example
    help_str += "\n\nEXAMPLE:\n" + get_example_config()
    
    return help_str
    

def help_menu(submenu = ""):
    menus = [help_example_config]
    
    match submenu:
        case "config":
            return help_example_config()
        case _: # no specific menu was chosen
            # Just print everything
            return "".join([m() for m in menus])



# ------------------------------------------- #
##=> DRIVER CODE
# ------------------------------------------- #


def gen_driver(arguments: list[str], options: list[tuple[str]]):
    # Check options
    for op in options:
        # Should always be at least one element, and should be option name
        match op[0]:
            case "-h" | "--help":
                submenu = ""
                if len(op) > 1:
                    submenu = op[1]
                print(help_menu(submenu))
                
    # Check arguments
    if len(arguments) > 0:
        # TODO: Remove this - it's a debug thing
        print("ARGUMENTS WERE GIVEN: {}".format(str(arguments)))
        
if __name__ == "__main__":
    example_json = """\
    {
        "projects" : ["myProj1"],
        "location" : ".",
        
        "myProj1" : {
            "compiler" : "clang++",
            "cpp" : "c++17",
            "kind" : "console",
            "location" : "%{WKS_DIR}/proj1",
            
            "bin" : "%{PRJ_DIR}/bin",
            
            "includeDirs" : [
                "%{PRJ_DIR}/src"
            ],
            
            "files" : [
                "src/*.cpp",
                "src/*.h"
            ]
        }
    }
    """
    generate_from_string(example_json)
