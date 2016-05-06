from distutils.core import setup, Extension
import numpy
from Cython.Distutils import build_ext
import os
os.environ["CC"] = "g++"
os.environ["CXX"] = "g++"
setup(
    cmdclass={'build_ext': build_ext},
    ext_modules=[Extension("pyForest",
                 sources=["_pyForest.pyx", "../FacadeForest.cpp","../utility.cpp","../Tree.cpp","../Forest.cpp","../IsolationForest.cpp"],
                 language="c++",
                 extra_compile_args=['-std=c++11'],
                 include_dirs=[numpy.get_include()])],
    )
