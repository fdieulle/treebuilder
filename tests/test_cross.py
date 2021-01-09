from typing import List
from treebuilder.cross import cross
from treebuilder.expand import expand


def __check(items: List, key: str, *args):
    assert [x[key] for x in items] == [x for x in args]


def test_with_empty_source():
    result = cross([], 'Name', ['foo', 'bar', 'other'])
    
    __check(result, 'Name', 'foo', 'bar', 'other')


def test_with_empty_values():
    result = expand([], 'Name', ['foo', 'bar', 'other'])
    result = cross(result, 'Value', [])

    assert len(result) == 0 # Because N x 0 = 0


def test_cross():
    result = expand([], 'Name', ['foo', 'bar', 'other'])
    result = cross(result, 'Value', [1, 2, 3])

    __check(result, 'Name', 'foo', 'bar', 'other', 'foo', 'bar', 'other', 'foo', 'bar', 'other')
    __check(result, 'Value', 1, 1, 1, 2, 2, 2, 3, 3, 3)


def test_cross_with_smaller_values():
    result = expand([], 'Name', ['foo', 'bar', 'other'])
    result = cross(result, 'Value', [1, 2])

    __check(result, 'Name', 'foo', 'bar', 'other', 'foo', 'bar', 'other')
    __check(result, 'Value', 1, 1, 1, 2, 2, 2)

    result = expand([], 'Name', ['foo', 'bar', 'other'])
    result = cross(result, 'Value', [1])

    __check(result, 'Name', 'foo', 'bar', 'other')
    __check(result, 'Value', 1, 1, 1)


def test_cross_with_longer_values():
    result = expand([], 'Name', ['foo', 'bar'])
    result = cross(result, 'Value', [1, 2, 3])

    __check(result, 'Name', 'foo', 'bar', 'foo', 'bar', 'foo', 'bar')
    __check(result, 'Value', 1, 1, 2, 2, 3, 3)

    result = expand([], 'Name', ['foo'])
    result = cross(result, 'Value', [1, 2, 3])

    __check(result, 'Name', 'foo', 'foo', 'foo')
    __check(result, 'Value', 1, 2, 3)
