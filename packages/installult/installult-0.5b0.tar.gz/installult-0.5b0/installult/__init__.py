import os
import subprocess
import sys
from os import system

def git(*args):
    return subprocess.check_call(["git"] + list(args))

def install(package):
    return subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "-r", package]
    )

__version__ = "0.5-beta"

package_name = "ffmpeg"
