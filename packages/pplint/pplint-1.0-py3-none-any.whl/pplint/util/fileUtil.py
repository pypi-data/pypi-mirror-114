import subprocess
import os

def get_project_path():
    ret = subprocess.run("git rev-parse --show-toplevel", shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         encoding="utf-8")
    if ret.returncode == 0:
        return ret.stdout.strip("\n")
    else:
        return os.getcwd()