# Python Clang Generator

Premake inspired project generator for clang compiler

The goal of this project is to have a quick way for me to generate `.clangd` files for my LSP as well as build/run scripts.
Making a tool that does this quickly with little effort will hopefully improve my linux workflow.

### Configuration

File generation can be controlled using a `.json` file containing information about how the workspaces and projects are structured and meant to be built

**Property Explanations:**
*   _WORKSPACE:_
    *   `"location"`: string
        >   Specifies the working directory of the workspace, relative to pwd of generate script. Can be accessed with "%{WKS_DIR}" and will be interpreted by the parser
    *   `"projects"`: array
        >   The names of other properties which should parsed and configured as projects.
    *   `"startproject"`: string
        >   Tells the workspace which project's binary should be run after compile.
        
*   _PROJECTS:_
    *   Note that the names of the project properties can be anything. As long as they're listed in the "projects" property for the workspace, they'll be generated.
    *   `"location"`: string
        >   Specifies the working directory of the project, from which other paths are derived (e.g. "files" property). Can be accessed with "%{PROJ_DIR}" and will be interpreted by the parser
    *   `"kind"`: string
        >   Specifies the type of binary to be compiled. Can be any of the following:
        *   `"console"`
            >   console app - directly executable.
        *   `"staticlib"`
            >   static library - contains definitions of symbols for compile-time linking
        *   `"sharedlib"`
            >   shared library - contains definitions of symbols for runtime linking
    *   `"bin"`: string
        >   Specifies the directory where binaries will be after compile
    *   `"files"`: array
        >   A list of which files the compiler should be looking for.
    *   `"defines"`: array
        >   A list of compiler definitions that should be used
    *   `"includeDirs"`: array
        >   A list of directories which should be included by the compiler
    *   `"links"`: array
        >   A list of projects binaries and/or libraries that should be linked

**Example configuration:**
This generates a workspace with two projects:
*   `project 1` builds as a staticlib
*   `project 2` builds as a console app/executable that links to `project 1`

```
{
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
}
```

