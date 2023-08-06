from setuptools import setup, Extension

kmerslib_core = Extension('kmerslib.core',
	sources=['kmerslib/core.cpp'],
	include_dirs = ['.'],
	libraries=['kmerslib'])

setup(name = 'kmerslib',
	author = 'Isaias May Canche', 
	author_email='isaias.mc@chetumal.tecnm.mx',
	version = '1.0.06',
	description="An example project showing how to build a pip-installable Python package that invokes custom CUDA/C++ code.",
	ext_modules=[kmerslib_core],
	packages=['kmerslib'],
	options={"bdist_wheel": {"universal": True}})
