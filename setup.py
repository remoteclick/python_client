from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='remoteclick',
    version='0.1',
    description='Remoteclick REST API Client.',
    author='www.remoteclick.ch',
    author_email='info@remoteclick.ch',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.6'
    ],
    keywords='remoteclick.ch remoteclick rest api client',
    packages=find_packages(exclude=['tests']),
    install_requires=['requests'],
)
