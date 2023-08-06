import setuptools

import kvgargs

setuptools.setup(
    name         = 'kvgargs',
    version      = kvgargs.__version__,
    author       = 'AXY',
    author_email = 'axy@declassed.art',
    description  = 'Grouped key-value command line argument parser',

    long_description = kvgargs.__doc__,
    long_description_content_type = 'text/x-rst',

    url = 'https://declassed.art/repository/kvgargs',

    py_modules = ['kvgargs'],

    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Development Status :: 4 - Beta',
        'Topic :: Software Development :: User Interfaces'
    ],

    python_requires = '>=3.6'
)
