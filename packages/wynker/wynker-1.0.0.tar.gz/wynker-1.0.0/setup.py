from os import read
from setuptools import setup, find_packages
from wynker import __author__, __author_email__, __version__
from glob import glob

with open('README.md') as f:
    readme = f.read()


setup(
    name='wynker',
    version=__version__,
    description="WYNKER provides Starter Kits for Flask.",
    long_description=readme,
    long_description_content_type='text/markdown',
    author=__author__,
    author_email=__author_email__,
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    data_files=[
        ('wynker', glob('templates/**/*', recursive=True))
    ],
    install_requires=["click==7.1.2", "colorama", "Jinja2"],
    entry_points={
        "console_scripts": [
            "wynker = wynker.bin.wynker:main"
        ]
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='flaskspot wynker wynker-cli starterkit flask boilerplate'
)