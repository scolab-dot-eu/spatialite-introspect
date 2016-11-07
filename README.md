# spatialite-introspect
Python library to do introspection in Sqlite/Spatialite databases.

Useful to get the table names, the column names of a specific table, the available geometry columns, etc, without needing to dig in SQL.

## Installation

```
pip install spatialiteintrospect
```

## Dependences

spatialite-introspect uses [sqlite3](https://docs.python.org/2/library/sqlite3.html), which should be included in any Python distribution since version 2.5.

## Usage

Basic usage:


```
from spatialiteintrospect import introspect as i
# open db connection
db = i.Introspect("mydb.sqlite")

# get all the tables in the db
db.get_tables()
# The result is an array of table names, e.g.: ['tbl1', 'tbl2', 'tbl3']

# finally, we need to close the database
db.close()

```

Available methods:


```
# get all the tables in the db
db.get_tables()
# The result is an array of table names, e.g.: ['tbl1', 'tbl2', 'tbl3']

# get all the tables that contain at least one geometry field
db.get_geometry_tables()
# The result is an array of table names, e.g.: ['tbl1', 'tbl3']

# get the geometry columns of a specific table
db.get_geometry_columns("tbl1")
# The result is an array of column names, e.g.: ['the_point_geom', 'the_line_geom']

# get the geometry columns of a specific tables, plus some information about the table containing it
db.get_geometry_columns_info("tbl1")
# The result is an array of tuples such as
#     [
#         ('tbl1', 'the_point_geom', 2, 4326, 1, ['fid'], ['fid', 'title', 'the_point_geom', 'the_line_geom']),
#         ('tbl1', 'the_line_geom', 2, 4326, 2, ['fid'], ['fid', 'title', 'the_point_geom', 'the_line_geom'])
#     ]
# The contents of each tuple is: (table_name, geom_column, coord_dimension, srid, geometry_type, key_columns, fields)

# It also works with no table filter:
db.get_geometry_columns_info()
# Result:
#     [
#         ('tbl1', 'the_point_geom', 2, 4326, 1, ['fid'], ['fid', 'title', 'the_point_geom', 'the_line_geom']),
#         ('tbl1', 'the_line_geom', 2, 4326, 2, ['fid'], ['fid', 'title', 'the_point_geom', 'the_line_geom']),
#         ('tbl3', 'geom', 2, 4326, 1, ['fid'], ['fid', 'author', 'date', 'geom'])
#     ]

# get the primary column(s) of a table
db.get_pk_columns("tbl2")
# The result is an array of the fields that compose the PK: ['country_cd', 'region_cd']

# get all the fields of a table
db.get_fields("tbl1")
# The result is an array of field names such as ['fid', 'title', 'the_point_geom', 'the_line_geom']

```

Note that the library expects Unicode strings on all the string params. Non unicode strings are also accepted if using ASCII-only characters. 


## Authors

Cesar Martinez Izquierdo - [Scolab](http://scolab.es)
