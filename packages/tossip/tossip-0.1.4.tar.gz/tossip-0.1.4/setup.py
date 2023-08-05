from setuptools import find_packages, setup

setup(
    name='tossip',
    packages=find_packages(include=['tossip']),
    url='https://github.com/liquiddevelopmentnet/tossip',
    version='0.1.4',
    description='A library to easily communicate with iOS Devices.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='LiquidDevelopment',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)