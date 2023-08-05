

""""""  # start delvewheel patch
def _delvewheel_init_patch_0_0_13():
    import os
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, '.'))
    if sys.version_info[:2] >= (3, 8):
        os.add_dll_directory(libs_dir)
    else:
        from ctypes import WinDLL
        with open(os.path.join(libs_dir, '.load-order-openjij-0.4.1')) as file:
            load_order = file.read().split()
        for lib in load_order:
            WinDLL(os.path.join(libs_dir, lib))


_delvewheel_init_patch_0_0_13()
del _delvewheel_init_patch_0_0_13
# end delvewheel patch

#from cxxjij import *
import cxxjij
from .__version import __version__
from .variable_type import SPIN, BINARY, Vartype, cast_vartype
from .sampler import Response
from .sampler import SASampler, SQASampler, CSQASampler
from .model import BinaryQuadraticModel, BinaryPolynomialModel
from .utils import solver_benchmark, convert_response
