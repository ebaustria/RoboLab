#!/usr/bin/env python3

"""
Simple stub that calls the 'real' deploy.py in the git submodule without an
additional path prefix. Passes along any parameters without modification.
For usage, optional arguments, syntax, etc. please refer to the README.md
of this repository, the 'robolab-deploy' submodule or the RoboLab Docs which
are accessible at https://robolab.inf.tu-dresden.de
This module: https://bitbucket.org/se-robolab/robolab-template
The submodule: https://bitbucket.org/se-robolab/robolab-deploy
Part of the RoboLab project
Systems Engineering Group, Faculty of Computer Science, TU Dresden
Copyright (c) 2017-2019 by Lutz Thies, Samuel Knobloch
Released under the MIT License
"""

import sys
import subprocess

# check if somebody forgot to use the --recursive flag
try:
    with open("./robolab-deploy/deploy.py") as f:
        pass
except FileNotFoundError:
    print("You forgot to use the --recursive flag while cloning this repository.")
    print("Please run: git submodule update --init --recursive")

# get the full executable path, because windows can't handle our shebang
PYTHON_EXECUTABLE = sys.executable
# it's basically a one-liner \o/
subprocess.call([PYTHON_EXECUTABLE, './robolab-deploy/deploy.py'] + sys.argv[1:])
