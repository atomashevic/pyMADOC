from setuptools import setup, find_packages

setup(
    name="pymadoc",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "requests",
        "tqdm",
    ],
    extras_require={
        'test': [
            'pytest>=6.0',
            'pytest-cov>=2.0',
        ],
    },
    author="Aleksandar Tomašević",
    author_email="atomashevic@gmail.com",
    description="Python package to download and combine parts of MADOC dataset",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/atomashevic/pyMADOC",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "pymadoc=pymadoc.pymadoc.cli:main",
        ],
    },
    test_suite="pymadoc.tests",
) 