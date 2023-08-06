from setuptools import setup

setup(
    name='webbuilder',
    version='1.1',
    packages=['webbuilder'],
    install_requires=[
        'requests',
        'importlib; python_version == "3.6"',
    ],
)