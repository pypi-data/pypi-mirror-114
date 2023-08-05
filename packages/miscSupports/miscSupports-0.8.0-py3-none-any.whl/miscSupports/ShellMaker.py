from miscSupports import validate_path
from pathlib import Path
import os


class Shell:
    def __init__(self, write_directory, write_name, make_directory=False):

        self._write_name = write_name
        self._write_dir = self._setup_directory(write_directory, write_name, make_directory)

    def _setup_directory(self, write_directory, write_name, make_directory):
        """Make a sub directory if requested, else just return the path of write_directory"""
        write_dir = validate_path(write_directory)

        if make_directory:
            try:
                os.mkdir(Path(write_dir, self._write_name))
            except FileExistsError:
                pass

            return Path(write_dir, write_name)
        else:
            return write_dir

    def create_shell_file(self):
        """
        Create an sh file called file_name
        """
        file = open(Path(self._write_dir, f"{self._write_name}.sh"), "w")
        file.write("#!/bin/bash\n\n")
        file.write("# Generate by pyGeneticPipe/Utils/Shell.py\n\n")
        return file
