from setuptools import setup, find_packages

VERSION = '0.1.0'
DESCRIPTION = 'An automatic differentiation package built as the final project for CS107'

with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

# Setting up
setup(
        name='autodiff_107',
        version=VERSION,
        author="Eryk Pecyna, Raphael Pellegrin, Jean-Guillaume Brasier, Xiyu Yang",
        author_email="erykpecyna@college.harvard.edu",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        package_dir={"": "src"},
        packages=find_packages(where="src"),
        python_requires=">=3.6",
        install_requires=[
            "numpy",
            "matplotlib",
            "networkx",
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
