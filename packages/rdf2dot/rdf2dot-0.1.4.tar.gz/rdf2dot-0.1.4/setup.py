from setuptools import setup
import sys

setup_requires = ['setuptools >= 30.3.0']

if {'pytest', 'test', 'ptr'}.intersection(sys.argv):
    setup_requires.append('pytest-runner')


setup(description="rdf2dot",
      version='0.1.4',
      include_package_data=True,
      setup_requires=setup_requires)
