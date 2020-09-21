<!-- [![Build Status](https://travis-ci.com/s-ball/MockSelector.svg?branch=master)](https://travis-ci.com/s-ball/MockSelector)
[![codecov](https://codecov.io/gh/s-ball/MockSelector/branch/master/graph/badge.svg)](https://codecov.io/gh/s-ball/MockSelector)
-->
# QtImgren

## Description

This is a GUI around the [pyimgren](https://pypi.org/project/pyimgren/) package. Currently it is able to rename camera images
via pyimgren forth and back. Its main feature is that it allows a manual
selection of the images to rename.

Of course buttons are there to allow default selections.

It is based on *profiles*. For `QtImgren`, a profile is what is required for
pyimgren configuration:

* a folder
* a source pattern to identify camera images (typically IMG*.JPG or DSCF*.JPG)
* a compatible with `datatime.strftime` pattern to build the new name from
the JPEG timestamp
* and of course a unique name

Thanks to pyimgren, it is possible to use a delta in minutes to cope with
a digital camera having a wrong time.

In order to make image selection easier, thumbnails can be displayed in the
main application window along with the current, future and original names. But
as image computation and display are expensive tasks, the display can be
turned off. Anyway, the computation is asynchronous, meaning that the
application can be used as soon as the currently displayed images are 
available.

## Installation

### From PyPI

    pip install qtimgren

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
    
Alternatively, you can use the `setup.py` script to build the unversioned
files without installing anything:

    python setup.py build

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

    qtimgren
   
## Internationalization

The application is natively written is English, and contains a French
translation of its IHM. It depends on Qt Linguist tools for generating the
binary file used at run-time. The required tool `lrelease` exists in the
Windows PySide2 distribution, but not in Linux or Mac ones. On those
platforms, you need a to install the Qt development tools and ensure that
they are accessible via the path.

Of course, if you install from a PyPi wheel, the compiled message files are
included as a resource.

At run time, the system default language is used by default, or can be
explicitly specified with the `--lang` option:

    qtimgren --lang=fr           # forces fr language
    qtimgren --lang=C            # forces native english language

## Disclaimer: alpha quality

It works, and is based on pyimgren which I have used for years. But corner
cases like renaming files more than once or trying to rename back images
with no registered original names need additional tests

## License

This work is licenced under a MIT Licence. See [LICENSE.txt](https://raw.githubusercontent.com/s-ball/MockSelector/master/LICENCE.txt)
