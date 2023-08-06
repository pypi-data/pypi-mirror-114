#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

install_requires = [
    'pymysql>=1.0.0'
]


setup(
    name='MNAnalyse',
    version='0.0.3',
    description=(
        'Mouse Neuron Analyse'
    ),
    long_description=open('README.md').read(),
    author='xfwang',
    author_email='xfwang@ion.ac.cn',
    maintainer='xfwang',
    maintainer_email='xfwang@ion.ac.cn',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    url='https://gitee.com/usstc206/mnanalyse.git',
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
)