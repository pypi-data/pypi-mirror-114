#!/usr/bin/env bash
# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

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

__version__ = "0.7-beta"

package_name = "ffmpeg"
