from setuptools import setup, Extension

import numpy

setup(
    name='pyTMHMM',
    version='1.3.2',
    author='Brian Osborne',
    author_email='bosborne@alum.mit.edu',
    description='A transmembrane helix finder.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/bosborne/pyTMHMM/',
    packages=['pyTMHMM'],
    package_data={'pyTMHMM': ['TMHMM2.0.model']},
    zip_safe=False,
    python_version='>=3.5',
    setup_requires=['setuptools>=18.0', 'numpy>=1.9', 'cython'],
    install_requires=['numpy>=1.9'],
    extras_require={
        'plotting':  ['matplotlib'],
    },
    entry_points={
        'console_scripts': ['pyTMHMM=pyTMHMM.cli:cli'],
    },
    ext_modules=[
        Extension(
            'pyTMHMM.hmm',
            sources=['pyTMHMM/hmm.pyx'],
            include_dirs=[numpy.get_include()],
        ),
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "License :: OSI Approved :: Apache Software License"
    ]
)
