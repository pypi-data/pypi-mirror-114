

""""""  # start delvewheel patch
def _delvewheel_init_patch_0_0_13():
    import os
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, '.'))
    if sys.version_info[:2] >= (3, 8):
        os.add_dll_directory(libs_dir)
    else:
        from ctypes import WinDLL
        with open(os.path.join(libs_dir, '.load-order-jij_cimod-1.3.2')) as file:
            load_order = file.read().split()
        for lib in load_order:
            WinDLL(os.path.join(libs_dir, lib))


_delvewheel_init_patch_0_0_13()
del _delvewheel_init_patch_0_0_13
# end delvewheel patch

try:
    import typing 
except ImportError:
    from typing_extensions import * 
import cxxcimod
import cimod.utils
import cimod.model 
import cimod.model.legacy
from cimod.vartype import SPIN, BINARY, Vartype
from cimod.model.binary_quadratic_model import make_BinaryQuadraticModel, make_BinaryQuadraticModel_from_JSON, BinaryQuadraticModel
from cimod.model.binary_polynomial_model import make_BinaryPolynomialModel, make_BinaryPolynomialModel_from_JSON, BinaryPolynomialModel
