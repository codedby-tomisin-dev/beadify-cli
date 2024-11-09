from cx_Freeze import setup, Executable

# Define your setup
setup(
    name="mycli",
    version="1.0",
    description="My CLI tool",
    executables=[Executable("src/cli/__main__.py", target_name="beads")],
)
