import sys, os

current_dir = os.getcwd().split('/')
if 'tests' in current_dir:
    current_dir.pop()
parent_dir = '/'.join(current_dir)
sys.path.insert(0, parent_dir)
