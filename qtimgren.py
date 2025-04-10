#  SPDX-FileCopyrightText: 2025-present s-ball <s-ball@laposte.net>
#  #
#  SPDX-License-Identifier: MIT

# The project can be compiled by Nuitka into a standalone executable with
# nuitka --standalone --python-flag="-m"  --output-dir=nuitka.out --report=nuitka-log.txt  --windows-icon-from-ico=icon/qtimgren.ico --product-version=0.5.0.0 --enable-plugin=pyside6  --include-data-files=venv/Lib/site-packages/PySide6/translations/*_fr.qm=PySide6/translations/ qtimgren

from qtimgren.__main__ import run

if __name__ == '__main__':
    run()
