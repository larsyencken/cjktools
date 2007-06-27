# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# __init__.py
# Lars Yencken <lars.yencken@gmail.com>
# vim: ts=4 sw=4 sts=4 et tw=78:
# Wed Jun 27 16:54:35 2007
#
#----------------------------------------------------------------------------#

"""
This package contains modules specific to processing the Japanese language, in
particular detecting scripts, converting between phonetic scripts, and
compensating for phonetic alterations in compounds.
"""

#----------------------------------------------------------------------------#

__all__ = [
        'kanaTable',
        'scripts',
        'alternations',
    ]
