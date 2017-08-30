#! /usr/bin/python3
"""
Add the source directories for the various pkgs to the front of path
so that, during test, import statements will find the source versions
of the pkg rather than any installed versions of the pkgs.

Environment variable setting can override this, to test the
installed versions of the pkgs.
"""

import os
import sys

magen_core_pkgs = [
    'magen_datastore',
    'magen_id_client',
    'magen_logaru',
    'magen_mongo',
    'magen_rest',
    'magen_stats',
    'magen_test_utils',
    'magen_utils' ]

# add submodules to path
# - walk list in reverse order to leave resultant path entries in orig order
def add_pkgs_to_path():
    magen_core_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
    for pkg in reversed(magen_core_pkgs):
        pkg_dir = magen_core_dir + pkg
        sys.path.insert(1, pkg_dir)

if os.getenv("MAGEN_CORE_TEST_INSTALLED"):
    # Unfortunately pytest captures this
    print("\nMAGEN-CORE TEST: WARNING:TESTING INSTALLED (NOT SOURCE) VERSION\n")
else:
    add_pkgs_to_path()
