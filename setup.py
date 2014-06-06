from setuptools import setup, find_packages

setup(
    name='modpeg',
    tests_require=['nose'],
    test_suite='nose.collector',
    packages=find_packages(exclude="*._test"),
)
