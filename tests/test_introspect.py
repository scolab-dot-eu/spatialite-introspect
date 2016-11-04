# -*- coding: utf-8 -*-
import pytest


@pytest.yield_fixture(scope="module")
def db():
    from spatialiteintrospect import introspect
    my_db = introspect.Introspect("tests/testdb.sqlite")
    yield my_db
    my_db.close()


def test_get_tables(db):
    tables = db.get_tables()
    assert len(tables) == 135
    assert 'tbl1' in tables
    assert 'tbl2' in tables
    assert 'tbl3' in tables
    assert 'tbl4' in tables
    assert u"tbl5strange:ñame_Ποταμός" in tables


def test_get_geometry_tables(db):
    tables = db.get_geometry_tables()
    assert [u'tbl1', u'tbl3', u'tbl4', u"tbl5strange:ñame_Ποταμός"] == tables


def test_get_geometry_columns(db):
    columns = db.get_geometry_columns("tbl1")
    assert [u'the_line_geom', u'the_point_geom'] == columns
    columns = db.get_geometry_columns(u"tbl5strange:ñame_Ποταμός")
    assert [u'geom'] == columns


def test_get_geometry_columns_info(db):
    tables = db.get_geometry_columns_info("tbl1")
    expected = [
        (
            u'tbl1', u'the_line_geom', 2, 4326, 2,
            [u'fid'],
            [u'fid', u'title', u'the_point_geom', u'the_line_geom']
        ),
        (
            u'tbl1', u'the_point_geom', 2, 4326, 1,
            [u'fid'],
            [u'fid', u'title', u'the_point_geom', u'the_line_geom']
        )
    ]
    assert expected == tables

    tables = db.get_geometry_columns_info()
    expected = (u'tbl4', u'geom', 2, 4326, 3, [], [u'name', u'geom'])
    assert expected == tables[3]


def test_get_pk_columns(db):
    cols = db.get_pk_columns("tbl2")
    assert [u'country_cd', u'region_cd'] == cols

    cols = db.get_pk_columns("tbl4")
    assert len(cols) == 0

    cols = db.get_pk_columns(u"tbl5strange:ñame_Ποταμός")
    assert [u'code'] == cols
