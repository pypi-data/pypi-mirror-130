from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'An automatic differentiation package built as the final project for CS107'
LONG_DESCRIPTION = 'TODO'

# Setting up
setup(
        name='autodiff_107',
        version=VERSION,
        author="Eryk Pecyna, Raphael Pellegrin, Jean-Guillaume Brasier, Xiyu Yang",
        author_email="erykpecyna@college.harvard.edu",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        intall_requires=["numpy"],
        url="https://github.com/cs107-errajexi/autodiff_107",
        classifiers=[
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
        ]
)
