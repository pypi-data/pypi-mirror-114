from setuptools import find_namespace_packages, setup

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'LICENSE'), encoding='utf-8') as f:
    license = f.read()

with open(path.join(HERE, 'README.rst'), encoding='utf-8') as f:
    readme = f.read()

setup(
    name='simulo',
    packages=['simulo', 'simulo.upload', 'simulo.auth', 'simulo.cli'],
    include_package_data=True,
    # py_modules = ['simulo', 'simulo.upload.data_upload', 'simulo.auth.authenticator'],
    version='0.2.6',
    description='The Simulo SDK',
    long_description = readme,
    long_description_content_type="text/x-rst",
    author='The Simulo Team',
    license=license,
    entry_points={
        'console_scripts': [
            'simulo = simulo.cli.runner:main',
        ],
    },
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    install_requires=["numpy", "requests", "requests_toolbelt", "PyJWT", "click"],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)