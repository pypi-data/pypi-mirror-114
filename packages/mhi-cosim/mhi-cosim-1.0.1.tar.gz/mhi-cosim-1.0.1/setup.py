#from distutils.core import setup, Extension
import re, codecs
from setuptools import setup, Extension

def get_version(version_file):
    with codecs.open(version_file, 'r') as fp:
        contents = fp.read()
    match = re.search(r"^VERSION = '([^']+)'", contents, re.M)
    if match:
        return match.group(1)
    raise RuntimeError("Unable to find version string")

version = get_version(r'src\mhi\cosim\__init__.py')

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
      version=version,
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
