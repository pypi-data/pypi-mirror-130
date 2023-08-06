from setuptools import setup

with open("README.rst") as f:
    long_description = f.read()

setup(
    name='pack_dataset',
    version='1.0.0',
    packages=['pack_dataset'],
    url='https://github.com/lnetw/pack_dataset',
    license='MIT License (MIT)',
    author='Maxim Ermak',
    author_email='max7ermak@gmail.com',
    long_description=long_description,
    install_requires=["pandas", "pymssql == 2.2.1"],
    description='This project contains a loader of a special data set, as a connection to the database using pymssql'
)
