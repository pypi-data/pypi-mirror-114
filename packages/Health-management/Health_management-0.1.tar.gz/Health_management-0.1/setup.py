import setuptools
from setuptools import *
with open("Readme.md", "r") as op:
    ld = op.read()
setup(name="Health_management",
      version="0.1",
      description="This is a package in which you can manage you health by making a simple program",
      long_description=ld,
      author="Anshu Gupta",
      url="https://github.com/Anshu370/Health_management_system",
      long_description_content_type="text/markdown",
      packages=setuptools.find_packages(),
      keywords=['health management python', 'health management system', 'python health management', 'health management'],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",],
      python_requires='>=3.9',
      py_modules=['HEALTH_MANAGEMENT'],
      package_dir={'': 'src'},
      install_requires=['datetime']
      )
