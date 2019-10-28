"""
Extracts TODO: notes from source code.

"""

import subprocess
import argparse
import re
import json


TODO_REGEXP = "^.*TODO:.*"


def grep_cmd(search_string):
    """Returns the command to run the selected grep program including flags.

    Prioritizes ripgrep (rg) and returns grep if rg is not installed.
    """
    cmd = ["grep", "-rn"]
    if not subprocess.run(
        "command -v rg", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    ).returncode:
        cmd = ["rg", "-n"]
    cmd.append(search_string)
    return cmd


def search_folder(folder):
    """Search folder for TODO notes and return the commands."""

    r = subprocess.run(
        grep_cmd(TODO_REGEXP), cwd=folder, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8"
    )
    return [
        m.groupdict()
        for m in re.finditer(r"^(?P<file>.*):(?P<line>\d*):.*TODO:\s*(?P<comment>.*)", r.stdout, re.M)
    ]


def main(folder):
    """Searches in folder and returns JSON"""
    return json.dumps(search_folder(folder), indent=2)


if __name__ == "__main__":
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("folder", help="Folder to look for TODO notes")
    args = args_parser.parse_args()

    print(main(args.folder))
