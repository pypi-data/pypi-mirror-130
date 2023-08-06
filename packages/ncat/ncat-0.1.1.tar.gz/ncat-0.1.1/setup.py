from setuptools import find_packages, setup

setup(
    name='ncat',
    packages=find_packages(include=['ncat']),
    version='0.1.1',
    description='Python wrapper for NGS Coordinate Conversion and Transformation Tool (NCAT) API.',
    author='Hayden Elza',
    url='https://github.com/HaydenElza/ncat-python',
    download_url='https://github.com/HaydenElza/ncat-python/archive/refs/tags/ncat-0.1.1.tar.gz',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==5.3.1'],
    test_suite='tests',
)