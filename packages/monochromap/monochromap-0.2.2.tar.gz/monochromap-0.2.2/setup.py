from setuptools import setup

# read the contents of README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='monochromap',
    packages=['monochromap'],
    version='0.2.2',
    description='A highly opinionated way to paint and plot black and white map',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='M Iqbal Tawakal',
    author_email='mit.iqi@gmail.com',
    url='https://github.com/mitbal/monochromap',
    keywords='static map image osm',
    classifiers=[],
    install_requires=[
        'Pillow',
        'requests',
        'futures;python_version<"3.2"'
    ]
)
