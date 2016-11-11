# -*- coding: utf-8 -*-

'''
    gvSIG Online.
    Copyright (C) 2007-2015 gvSIG Association.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
'''
@author: Cesar Martinez <cmartinez@scolab.es>
'''

"""
Spatialite_introspect: a standalone library to do Sqlite/Spatialite
introspection using Pythonic style.

This library easily gets the table names, the column names of a
specific table, the available geometry columns, etc.
"""


import sqlite3
import os

def connect(file_path, create=False):
    return Introspect(file_path, create)

class Introspect:
    QUOTE_CHAR = "'"

    def __init__(self, file_path, create=False):
        if not create and not self.is_sqlite3(file_path):
            raise InvalidSqlite3Database()
        self.conn = sqlite3.connect(file_path)
        self.cursor = self.conn.cursor()

    def is_sqlite3(self, file_path):
        if not os.path.isfile(file_path):
            return False
        if os.path.getsize(file_path) < 100: # SQLite database file header is 100 bytes
            return False
        with open(file_path, 'rb') as fd:
            header = fd.read(100)
            return header[:16] == b'SQLite format 3\x00'

    def get_tables(self):
        self.cursor.execute("""
        SELECT name FROM sqlite_master
        """)
        return [r[0] for r in self.cursor.fetchall()]

    def get_geometry_tables(self):
        self.cursor.execute("""
        SELECT f_table_name FROM geometry_columns
        GROUP BY f_table_name;
        """)
        return [r[0] for r in self.cursor.fetchall()]

    def get_geometry_columns(self, table):
        self.cursor.execute(u"""
        SELECT f_geometry_column
        FROM geometry_columns
        WHERE f_table_name = ?
        """, [table])
        return [r[0] for r in self.cursor.fetchall()]

    def get_geometry_columns_info(self, table=None):
        """
        Returns a tuple formed of:
         (table_name, geom_column, coord_dimension, srid, geometry_type, key_columns, fields)
        """
        if table:
            self.cursor.execute(u"""
            SELECT f_table_name, f_geometry_column, coord_dimension, srid, geometry_type
            FROM geometry_columns
            WHERE f_table_name = ?
            """, [table])
        else:
            self.cursor.execute(u"""
            SELECT f_table_name, f_geometry_column, coord_dimension, srid, geometry_type
            FROM geometry_columns
            """)

        return [
            (
                r[0], r[1], r[2], r[3], r[4],
                self.get_pk_columns(r[0]), self.get_fields(r[0])
            )
            for r in self.cursor.fetchall()
        ]

    def get_pk_columns(self, table):
        """
        Gets the field names that form the primary key of a table. The returned
        value is a list of strings.
        The order of each field on the list matches the order of the primary key
        on the table
        """
        if self.QUOTE_CHAR in table:
            raise InvalidIdentifierException
        query = u"pragma table_info('{0}')".format(table)
        result = self.conn.execute(query).fetchall()
        # Primary keys have a value > 0 in the primary key column
        # The value also determines the order of the columns in the PK
        result.sort(key=lambda x: x[5])
        return [r[1] for r in result if r[5] > 0]

    def get_fields(self, table):
        """
        Gets the field names of a table as a list of strings
        """
        if self.QUOTE_CHAR in table:
            raise InvalidIdentifierException
        query = u"pragma table_info('{0}')".format(table)
        result = self.conn.execute(query).fetchall()
        return [r[1] for r in result]

    def close(self):
        """
        Closes the connection. The Introspect object can't be used afterwards
        """
        self.conn.close()


class InvalidIdentifierException(Exception):
    pass

class InvalidSqlite3Database(Exception):
    pass
