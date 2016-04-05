#!/usr/bin/env python
"""
Base django runner module
"""
import sys
import os


PATHS = ('../contrib',)

def rel(*x):
    """Method for getting abspath from current dir and nested files
    """
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

for path in PATHS:
    path = rel(path)
    if path not in sys.path:
        sys.path.insert(0, path)

try:
    import settings  # Assumed to be in the same directory.
except ImportError:
    sys.stderr.write("""Error: Can't find the file 'settings.py' in the
            directory containing %r. It appears you've customized things.\n
            You'll have to run django-admin.py, passing it your settings
            module.\n(If the file settings.py does indeed exist, it's causing
            an ImportError somehow.)\n""" % __file__)
    sys.exit(1)

from django.core.management import execute_manager
if __name__ == "__main__":
    execute_manager(settings)
