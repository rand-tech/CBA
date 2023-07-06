import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path


def main(input_filename, output_dir=None):
    ghidra_install_path = Path(os.getenv("GHIDRA_INSTALL_PATH", "tools/ghidra"))
    ghidra_headless_path = ghidra_install_path / 'support' / 'analyzeHeadless'
    ghidra_scripts_path = os.path.join(os.getcwd(), 'tools', 'ghidraScripts')

    create_ghidra_scripts_directory(ghidra_scripts_path)

    # get the path of the input file, change the 'file' to 'output'
    output_dir = os.path.dirname(input_filename) if output_dir is None else output_dir

    decompile_script(ghidra_headless_path, ghidra_scripts_path, input_filename, output_dir)


def create_ghidra_scripts_directory(ghidra_scripts_path):
    """Creates a directory at the specified path if it doesn't exist."""
    os.makedirs(ghidra_scripts_path, exist_ok=True)


def decompile_script(ghidra_headless_path, ghidra_scripts_path, input_filename, output_folder):
    """Decompile the input file using Ghidra headless analyzer."""
    with tempfile.TemporaryDirectory() as temp_directory:
        project_directory = tempfile.TemporaryDirectory(dir=temp_directory)
        filename = os.path.basename(input_filename)

        code_file = os.path.join(output_folder, f"{filename}.ghidra.cxx")
        capa_file = os.path.join(output_folder, f"{filename}.json")
        gzf_file = os.path.join(output_folder, f"{filename}.gzf")

        # fmt: off
        decompile_command = [
            f"{ghidra_headless_path}",
            project_directory.name,
            "temp",
            "-import", input_filename,
            "-scriptPath", f"{ghidra_scripts_path}",
            "-postScript", f"{ghidra_scripts_path}/capaexplorer.py", capa_file,
            "-postScript", f"{ghidra_scripts_path}/gzfExporter.py", gzf_file,
            "-postScript", f"{ghidra_scripts_path}/exportCpp.py", code_file,
        ]
        # fmt: on

        decomp_process = subprocess.run(decompile_command, capture_output=True)
        if decomp_process.returncode != 0 or not os.path.exists(gzf_file):
            print("ERROR")
            print(f'{decomp_process.stdout.decode()}\n{"= "*80}\n{decomp_process.stderr.decode()}\n{"= "*80}')


if __name__ == "__main__":
    main(sys.argv[1])