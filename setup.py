from setuptools import setup, find_packages

setup(
    name='my-behave-tests',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'run-behave=my_behave_tests.runner:main'
        ]
    }
)