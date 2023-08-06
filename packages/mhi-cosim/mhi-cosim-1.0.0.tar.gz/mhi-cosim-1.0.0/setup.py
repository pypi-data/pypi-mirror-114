#from distutils.core import setup, Extension
from setuptools import setup, Extension

cosim = Extension('_cosim',
                  sources=[r'src\ext\cosim.c',
                           r'src\ext\EmtCoSim\EmtCoSim.c',
                           ],
                  #include_dirs=['src/ext/EmtCoSim',
                  #              ],
                  )

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(name='mhi-cosim',
      version='1.0.0',
      description='MHI Cosimulation Module',
      long_description=long_description,
      long_description_content_type="text/x-rst",
      ext_modules=[cosim],
      ext_package='mhi.cosim',
      package_dir={'': 'src'},
      packages=['mhi.cosim'],
      requires=['wheel'],
      python_requires='>=3',
      author='Manitoba Hydro International Ltd.',
      author_email='pscad@mhi.ca',
      url='https://www.pscad.com/webhelp-v5-al/index.html',
      license="BSD License",

      classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
      ],
      )
