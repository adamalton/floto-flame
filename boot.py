import sys
from os.path import dirname, abspath, join

PROJECT_DIR = dirname(abspath(__file__))
SITEPACKAGES_DIR = join(PROJECT_DIR, "libs")

def fix_path():
    if SITEPACKAGES_DIR not in sys.path:
        sys.path.insert(1, SITEPACKAGES_DIR)
