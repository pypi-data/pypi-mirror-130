# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Vinay Sajip.
# Licensed to the Python Software Foundation under a contributor agreement.
# See LICENSE.txt and CONTRIBUTORS.txt.
#

import distutils.core
from os.path import join, dirname

import distlib


class TestCommand(distutils.core.Command):
    user_options = []

    def run(self):
        import sys

        sys.path.append(join(dirname(__file__), 'tests'))
        import test_all
        sys.exit(test_all.main())

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass


distutils.core.setup(
    name='distlib',
    version=distlib.__version__,
    author='Vinay Sajip',
    author_email='vinay_sajip@red-dove.com',
    url='https://bitbucket.org/pypa/distlib',
    download_url=('https://bitbucket.org/pypa/distlib/downloads/'
                  'distlib-' + distlib.__version__ + '.zip'),
    description='Distribution utilities',
    long_description=('Low-level components of distutils2/packaging, '
                      'augmented with higher-level APIs for making packaging easier.'),
    license='Python license',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development',
    ],
    platforms='any',
    packages=[
        'distlib'
    ],
    package_data={
        'distlib': ['t32.exe', 't64.exe', 'w32.exe', 'w64.exe',
                    't64-arm.exe', 'w64-arm.exe'],
    },
    cmdclass={
        'test': TestCommand,
    },
)
