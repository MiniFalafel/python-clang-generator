### Analysis


**Clang Build Script:**
*   A bash script that calls the `clang` compiler. Maybe in the future, we can allow users to specify which compiler they want to use.
*   After running the build command, the script will also run the executable file that was generated (if the user specifies it in their `.json` file)


**Clangd LSP `.clangd` file**
*   I'm honestly not super familiar with how this works, but i _think_ this informs the `clangd` LSP of the includes, config, etc. that the user specifies.
*   This is important because otherwise, the LSP thinks that the includes don't exist and shows errors in the code editor.

### Design


##### Build command (per project):
*   Gathers files to build and the output/`bin` directory.
    -   Note that while header files (`**.h`) should be ignored as they don't contain implementation code, I'm sure that implementation code might end up in a header file for one reason or another, so I'm actually opting to **_include_** these files in the build command (see example below).
*   Gathers include directories, linking directories, and linking names.
*   Calls `clang` or `clang++` compiler with options to specify all of these things.

output should look something like this:
```bash
clang++ src/my_file.cpp src/my_file2.cpp src/a_header.h -o path/to/binary/my_file -I include/dir/1 -I include/dir/2 -L linking/dir/1 -lname_of_linked_binary
```

Pseudocode:
```c++
string getProjOutputFilename(project)
{
    bin_dir = project.get_property("bin");
    return format("{}/{}", bin_dir, project.get_name()).get_str();
}

string parameterize(format_template, paths)
{
    output = "";
    for (path : paths)
    {
        output += format(format_templace, path);
    }
    return output;
}

string getProjFileArgs(project)
{
    files = project.get_property("files"); // an array of filepaths
    // parameterize
    return parameterize(" {}", files);
}

string getProjIncludes(project)
{
    include_dirs = project.get_property("includeDirs");
    return parameterize(" -I {}", include_dirs);
}

string getProjLinkDirs(project)
{
    link_dirs = project.get_property("linkDirs");
    return parameterize(" -L {}", link_dirs);
}

string getProjLinkNames(project)
{
    link_names = project.get_property("links");
    return parameterize(" -l{}", link_names);
}

// ACTUAL GENERATE FUNCTION
void generateClangBuild(project)
{
    command_format = "{compiler} {files} -o {output_file} {include_dirs} {link_dirs} {lib_names}"
    
    // Get all of the data to format the command
    compiler = project.get_property("compiler");
    files = getProjFileArgs(project);
    output = getProjOutputFilename(project);
    
    includes = getProjIncludes(project);
    link_dirs = getProjLinkDirs(project);
    links = getProjLinkNames(project);
    
    return format(command_format, compiler, files, output, inclides, link_dirs, links).get_str();
}
```



### Tests + Debugging




