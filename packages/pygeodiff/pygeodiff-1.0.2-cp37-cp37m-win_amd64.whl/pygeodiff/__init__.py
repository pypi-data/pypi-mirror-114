# -*- coding: utf-8 -*-
"""
    pygeodiff
    -----------
    This module provides tools for create diffs of geospatial data formats
    :copyright: (c) 2019 Peter Petrik
    :license: MIT, see LICENSE for more details.
"""


""""""  # start delvewheel patch
def _delvewheel_init_patch_0_0_13():
    import os
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'pygeodiff.libs'))
    if sys.version_info[:2] >= (3, 8):
        os.add_dll_directory(libs_dir)
    else:
        from ctypes import WinDLL
        with open(os.path.join(libs_dir, '.load-order-pygeodiff-1.0.2')) as file:
            load_order = file.read().split()
        for lib in load_order:
            WinDLL(os.path.join(libs_dir, lib))


_delvewheel_init_patch_0_0_13()
del _delvewheel_init_patch_0_0_13
# end delvewheel patch



from .main import GeoDiff
from .geodifflib import (
    GeoDiffLibError,
    GeoDiffLibConflictError,
    GeoDiffLibUnsupportedChangeError,
    GeoDiffLibVersionError,
    ChangesetEntry,
    ChangesetReader,
    UndefinedValue,
)