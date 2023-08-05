from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
	name='nfl_data_py',
	version='0.0.1',
	description='Package for working with NFL data',
    author='cooperdff',
    author_email='cooper.dff11@gmail.com',
    url='https://github.com/cooperdff/nfl_data_py',
	packages=['nfl_data_py'],
	package_dir={'nfl_data_py': 'src/nfl_data_py'},
    install_requires=[
        'numpy>1',
        'pandas>1',
        'datetime>3.5',
        'fastparquet>0.5',
        'python-snappy',
        'snappy>1',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown'
)