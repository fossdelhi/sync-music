#!/usr/bin/env python3
import sys
import os

"""
File to add the path of project directories with respect to "tests" directory
to access source files as modules.

Assumings tests are running either from project root or from "tests" directory.
"""

project_directory = os.getcwd().split('/')
if 'tests' in project_directory:
    project_directory = project_directory[:len(os.getcwd().split('/'))-1]
project_directory = '/'.join(project_directory)
if project_directory not in sys.path:
    sys.path.append(project_directory)

# adding required directories for tests in path
sys.path.append(project_directory+'/src')
