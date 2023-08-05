import os
from p1_helpers import __version__
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

ROOT = os.path.dirname(__file__)
INSTALL_REQUIRES = [
    "pandas >= 1.1.1",
    "boto3 >= 1.14.51",
    "tqdm >= 4.61.2",
]
TEST_REQUIRES = ["pytest>=5.0.0"]


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    version=__version__,
    name="p1_helpers",
    description="A corporate helper package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[
        "p1_helpers",
        "particle",
        "particleone",
        "particle.one",
    ],
    author="ParticleOne Team",
    author_email="malanin@particle.one",
    maintainer="",
    maintainer_email="",
    url="https://github.com/ParticleDev/p1_helpers",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    install_requires=INSTALL_REQUIRES,
    tests_require=TEST_REQUIRES,
    python_requires=">= 3.7",
    test_suite="pytest",
    packages=find_packages(exclude=("test")),
)
