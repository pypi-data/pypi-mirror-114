import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(name='hierarpy',
      version='1.1.2',
      description='A library for hierarchical configuration in Python.',
      long_description=README,
      long_description_content_type='text/markdown',
      url='https://github.com/rodrigo-castellon/hierarpy',
      author='Rodrigo Castellon',
      author_email='rjcaste@stanford.edu',
      license='MIT',
      install_requires=['addict', 'PyYAML'],
      include_package_data=True,
      packages=['hierarpy'])
