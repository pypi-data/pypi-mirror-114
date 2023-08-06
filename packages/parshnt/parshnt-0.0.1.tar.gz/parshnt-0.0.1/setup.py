
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

__version__ = '0.0.1'

setup(
    name="parshnt",
    description="A test PyPi package",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/parshnt",
    author="Parshant",
    author_email="hi.parshant@gmail.com",
    python_requires=">=3.5",
    classifiers=[
        'Environment :: Plugins',
        'License :: OSI Approved :: Apache Software License',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators"
    ],
    keywords='dummy',
    install_requires=[],
    include_package_data=True,
    packages=find_packages(),
    license='Apache License 2.0',
    version=__version__,
)
