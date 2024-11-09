from cx_Freeze import setup, Executable

build_exe_options = {
    "include_files": [("src/cli/scripts", "scripts")]
}

# Define your setup
setup(
    name="mycli",
    version="1.0",
    description="My CLI tool",
    options={"build_exe": build_exe_options},
    executables=[Executable("src/cli/__main__.py", target_name="beads")],
)
