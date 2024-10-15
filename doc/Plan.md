### Analysis

**Clang Build Script:**
*   A bash script that calls the `clang` compiler. Maybe in the future, we can allow users to specify which compiler they want to use.
*   After running the build command, the script will also run the executable file that was generated (if the user specifies it in their `.json` file)


**Clangd LSP `.clangd` file**
*   I'm honestly not super familiar with how this works, but i _think_ this informs the `clangd` LSP of the includes, config, etc. that the user specifies.
*   This is important because otherwise, the LSP thinks that the includes don't exist and shows errors in the code editor.

### Design



### Tests + Debugging


