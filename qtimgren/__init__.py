#  SPDX-FileCopyrightText: 2025-present s-ball <s-ball@laposte.net>
#  #
#  SPDX-License-Identifier: MIT

try:
    from .version import version as __version__
except ImportError:
    __version__ = '0.0.0'

__all__ = [__version__]
