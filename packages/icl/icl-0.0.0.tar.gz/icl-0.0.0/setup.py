from setuptools import *


setup(
    name='icl',
    version='0.0.0',
    packages=['icl'],
    package_dir={'icl': 'inc/icl'},
    install_requires=['infinity>=1.5'],
    python_requires='>=3.8',

    url='https://github.com/happyxianyu/icl',
    license='Apache License 2.0',
    author='happyxianyu',
    author_email=' happyxianyu623@outlook.com',
    description='Interval Container Library'
)
