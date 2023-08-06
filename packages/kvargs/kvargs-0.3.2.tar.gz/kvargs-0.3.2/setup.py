import setuptools

import kvargs

setuptools.setup(
    name         = 'kvargs',
    version      = kvargs.__version__,
    author       = 'AXY',
    author_email = 'axy@declassed.art',
    description  = 'Key-value command line argument parser',

    long_description = kvargs.__doc__,
    long_description_content_type = 'text/x-rst',

    url = 'https://declassed.art/repository/kvargs',

    py_modules = ['kvargs'],

    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Development Status :: 5 - Production/Stable',
        'Topic :: Software Development :: User Interfaces'
    ],

    python_requires = '>=3.6'
)
