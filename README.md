<!-- [![Build Status](https://travis-ci.com/s-ball/MockSelector.svg?branch=master)](https://travis-ci.com/s-ball/MockSelector)
[![codecov](https://codecov.io/gh/s-ball/MockSelector/branch/master/graph/badge.svg)](https://codecov.io/gh/s-ball/MockSelector)
-->
# QtImgren

## Description

This is a GUI around the [pyimgren](https://pypi.org/project/pyimgren/) package. This is currently only a work in progress...

## Installation

### From PyPI

Not currently available...

### From Github

This is the recommended way if you want to contribute or simply tweak
`QtImgren` to your own requirements. You can get a local copy by
downloading a zipfile but if you want to make changes, you should
 rather clone the repository to have access to all `git` goodies:

    git clone https://github.com/s-ball/qtimgren.git

You can then install it in your main Python installation or in a venv with:

    pip install -e .

or on Windows with the launcher:

    py -m pip install -e .
    
`pip` should be used to install it for the first time in order to have
`setuptools-scm` to generate the `version.py` file from git metadata.
Once this is done, `setup.py` can be used with no special issue.

Alternatively you can manually install `setuptools-scm`:

    pip install setuptools-scm
    python setup.py install

#### Special handling of `version.py`:

`QtImgren` relies on `setuptools-scm` to automatically extract a
version number from git metadata and store it in a `version.py` file
for later use. The requires the availability of both `git` (which should
not be a problem when the project is downloaded from Github), and
`setuptools-scm`. If it fails because one is not available or because
git metadata is not there (if you only downloaded a zip archive from
Github), the version is set to 0.0.0

For that reason, if you do not use git to download the sources, you
should download a source distribution from PyPI, because the latter
contains a valid `version.py`

`pip` uses the `pyproject.toml` file with respect to PEP-518 and
PEP-517 to know that `setuptools-scm` is required before the build.

## Basic use

Once installed, you can run the application:

```
    python -m QtImgren
```


## Disclaimer: pre-alpha quality

As already said, this is currently just a work in progress.
## License

This work is licenced under a MIT Licence. See [LICENSE.txt](https://raw.githubusercontent.com/s-ball/MockSelector/master/LICENCE.txt)
