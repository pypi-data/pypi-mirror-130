from setuptools import setup, find_packages

VERSION = '0.0.5'
DESCRIPTION = 'An automatic differentiation package built as the final project for CS107'
LONG_DESCRIPTION = 'This package builds upon and is an extension of numpy. It is meant to allow for almost all operations permitted by numpy but can differentiate results automatically. The packages supports both forward and backward mode and will even compute jacobians. Full documentation can be found at the github repo linked on this page.'

# Setting up
setup(
        name='autodiff_107',
        version=VERSION,
        author="Eryk Pecyna, Raphael Pellegrin, Jean-Guillaume Brasier, Xiyu Yang",
        author_email="erykpecyna@college.harvard.edu",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        setup_requires=["numpy>=1.19.5"],
        intall_requires=[
            "numpy>=1.119.5",
            "matplotlib>=3.3.4",
            "networkx>=2.5.1",
        ],
        url="https://github.com/cs107-errajexi/autodiff_107",
        classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Education",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
        ]
)
