[![Build Status](https://travis-ci.com/s-ball/qtimgren.svg?branch=master)](https://travis-ci.com/s-ball/qtimgren)
<!-- [![codecov](https://codecov.io/gh/s-ball/MockSelector/branch/master/graph/badge.svg)](https://codecov.io/gh/s-ball/MockSelector)
-->
# qtimgren

## Description

This is a GUI around the [pyimgren](https://pypi.org/project/pyimgren/) package.
Currently, it is able to rename camera images
via pyimgren forth and back. Its main feature is that it allows a manual
selection of the images to rename.

Of course buttons are there to allow default selections.

It is based on *profiles*. For `qtimgren`, a profile is what is required for
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
available. Starting with the 0.5.x series, thumbnails are statically cached
in a local SQLite database.

## Installation

### Direct installation on Windows

Thanks to PyInstaller and InnoSetup, an installer and a portable zip file
are available on [GitHub](https://github.com/s-ball/qtimgren/releases).

That way you have no dependencies, not even on Python.

### From PyPI

    pip install qtimgren

### From GitHub

This is the recommended way if you want to contribute or simply tweak
`qtimgren` to your own requirements. You can get a local copy by
downloading a zipfile but if you want to make changes, you should
 rather clone the repository to have access to all `git` goodies:

    git clone https://github.com/s-ball/qtimgren.git

You can then install it in your main Python installation or in a venv with:

    pip install -e .

or on Windows with the launcher:

    py -m pip install -e .
    
#### Special handling of `version.py`:

`QtImgren` relies on `hatch-vcs` to automatically extract a
version number from git metadata and store it in a `version.py` file
for later use. This requires the availability of both `git` (which should
not be a problem when the project is downloaded from GitHub), and
an installation via `pip` or a build through a PEP518 compatible tool.
If it fails because one is not available or because
git metadata is not there (if you only downloaded a zip archive from
GitHub), the version is set to 0.0.0

For that reason, if you do not use git to download the sources, you
should download a source distribution from PyPI, because the latter
contains a valid `version.py`

`pip` uses the `pyproject.toml` file with respect to PEP-518 and
PEP-517 to know that `hatch-vcs` is required before the build.

## Basic use

Once installed, you can run the application:

    qtimgren
   
## Internationalization

The application is natively written is English, and contains a French
translation of its IHM. It depends on Qt Linguist tools for generating the
binary file used at run-time. This is automatically done at build or install
time by the `hatch-pyside` project.

Of course, if you install from a PyPi wheel, the compiled message files are
included as a resource.

At run time, the system default language is used by default, or can be
explicitly specified with the `--lang` option:

    qtimgren --lang=fr           # forces fr language
    qtimgren --lang=C            # forces native english language

## Contributions

Contributions are welcome, including translations or just issues on GitHub.
Problems are expected to be documented so that they can be reproduced. But
I only develop this on my free time, so I cannot guarantee quick answers...

## Disclaimer: beta quality

All functionalities are now implemented, and the underlying pyimgren module
has been used for years. I trust it enough to handle my own photographs
with it. Yet it still lacks a decent documentation, and
has not been extensively tested

## License

This work is licenced under a MIT Licence. See [LICENSE.txt](https://raw.githubusercontent.com/s-ball/MockSelector/master/LICENCE.txt)
