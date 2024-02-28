import numpy
from Cython.Build import cythonize
from setuptools import setup, Extension


ext = [
    Extension(
        "pyTMHMM.hmm",
        ["pyTMHMM/hmm.pyx"],
    )
]

setup(
    name="pyTMHMM",
    version="1.3.5",
    license="MIT License",
    author="Brian Osborne",
    author_email="bosborne@alum.mit.edu",
    description="A transmembrane helix finder.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/bosborne/pyTMHMM/",
    packages=["pyTMHMM"],
    package_data={"pyTMHMM": ["TMHMM2.0.model"]},
    zip_safe=False,
    python_version=">=3.5",
    setup_requires=["setuptools>=18.0", "numpy>=1.9", "cython"],
    install_requires=["numpy>=1.9"],
    extras_require={
        "plotting": ["matplotlib"],
    },
    entry_points={
        "console_scripts": ["pyTMHMM=pyTMHMM.cli:cli"],
    },
    include_dirs=[numpy.get_include(),"."],
    ext_modules=cythonize(ext),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "License :: OSI Approved :: MIT License",
    ],
)
