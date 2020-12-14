from setuptools import setup, Extension

import numpy

setup(
    name='tmhmm.py',
    version='1.3.2',
    author='Brian Osborne',
    author_email='briano@bioteam.net',
    description='A transmembrane helix finder.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',

    url='https://github.com/bosborne/tmhmm.py/',
    packages=['tmhmm'],
    package_data={'tmhmm': ['TMHMM2.0.model']},
    zip_safe=False,

    python_version='>=3.5',

    setup_requires=['setuptools>=18.0', 'numpy>=1.9', 'cython'],
    install_requires=['numpy>=1.9'],
    extras_require={
        'plotting':  ['matplotlib'],
    },

    entry_points={
        'console_scripts': ['tmhmm=tmhmm.cli:cli'],
    },

    ext_modules=[
        Extension(
            'tmhmm.hmm',
            sources=['tmhmm/hmm.pyx'],
            include_dirs=[numpy.get_include()],
        ),
    ],
)
