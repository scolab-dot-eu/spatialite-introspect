# -*- coding: utf-8 -*-
"""Python library for easily retrieving table names, geometry columns, geometry
  tables, etc from a Spatialite database"""

from . import metadata

from .introspect import connect

__version__ = metadata.version
__author__ = metadata.authors[0]
__license__ = metadata.license
__copyright__ = metadata.copyright
