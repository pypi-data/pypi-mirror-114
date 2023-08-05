from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='graph-dfs',
    version='0.0.3',
    description='Module for creating graphs and performing depth first search.',
    py_modules=['dfs'],
    package_dir={'': 'src'},
    url="https://github.com/daniel-ufabc/graph-dfs",
    author="Daniel M. Martin",
    author_email="danielmmartin@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    extra_requires={
        'dev': [
            'pytest>=3.7',
        ]
    }
)
