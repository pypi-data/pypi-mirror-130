"""Setup for the moconf package."""

import setuptools


with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author="Sean Jabro",
    author_email="sjabro@morpheusdata.com",
    name='moconf',
    license="Apache 2.0",
    description='moconf is a package for configuring a Morpheus appliance.',
    version='v0.0.14',
    long_description=README,
    url='https://github.com/morpheus-training/moconf',
    packages=setuptools.find_packages(),
    install_requires=[
        'requests>=2.21.0',
        'urllib3'
        ]
)