from setuptools import setup, Extension
import pybind11
import numpy

ext_modules = [
    Extension(
        'monte_carlo',  
        ['monte_carlo.cpp'],  
        include_dirs=[
            pybind11.get_include(), numpy.get_include(),
            'C:/Users/ASUS/Desktop/C++/python/OptionsModel/', 
        ],

        language='c++'
    ),
]

setup(
    name='monte_carlo',
    version='1.0',
    description='Monte Carlo simulation',
    ext_modules=ext_modules,
)
