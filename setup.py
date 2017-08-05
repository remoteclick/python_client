from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='iotclient',
    version='0.1',
    packages=['iotclient'],
    url='http://www.iotcloud.local',
    license='',
    author='BLANKE automation GmbH',
    author_email='info@blanke.ch',
    description='IoT Client Library for the IoT-Cloud API.'
)

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='iotclient',
    version='0.1.0',
    description='IoT Client Library for the IoT-Cloud API.',
    long_description=long_description,
    url='https://github.com/....',
    author='BLANKE automation GmbH',
    author_email='info@blanke.ch',
    license='MIT',
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: API Clients',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='iot api client blanke automation',

    packages=find_packages(exclude=['tests']),

    install_requires=['requests'],
)
