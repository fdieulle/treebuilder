from typing import List
from treebuilder.expand import expand


def __check(items: List, key: str, *args):
    assert [x[key] for x in items] == [x for x in args]


def test_with_empty_source():
    result = expand([], 'Name', ['foo', 'bar', 'other'])
    
    __check(result, 'Name', 'foo', 'bar', 'other')


def test_with_empty_values():
    result = expand([], 'Name', ['foo', 'bar', 'other'])
    result = expand(result, 'Value', [])

    __check(result, 'Name', 'foo', 'bar', 'other')
    assert all(['Value' not in x for x in result])


def test_expand():
    result = expand([], 'Name', ['foo', 'bar', 'other'])
    result = expand(result, 'Value', [1, 2, 3])

    __check(result, 'Name', 'foo', 'bar', 'other')
    __check(result, 'Value', 1, 2, 3)


def test_expand_with_smaller_values():
    result = expand([], 'Name', ['foo', 'bar', 'other'])
    result = expand(result, 'Value', [1, 2])

    __check(result, 'Name', 'foo', 'bar', 'other')
    __check(result, 'Value', 1, 2, 1)

    result = expand([], 'Name', ['foo', 'bar', 'other'])
    result = expand(result, 'Value', [1])

    __check(result, 'Name', 'foo', 'bar', 'other')
    __check(result, 'Value', 1, 1, 1)
    

def test_expand_with_smaller_values_and_repeat():
    result = expand([], 'Name', ['foo', 'bar', 'other', 'foo', 'bar', 'other'])
    result = expand(result, 'Value', [1, 2])

    __check(result, 'Name', 'foo', 'bar', 'other', 'foo', 'bar', 'other')
    __check(result, 'Value', 1, 2, 1, 2, 1, 2)

    result = expand([], 'Name', ['foo', 'bar', 'other', 'foo', 'bar'])
    result = expand(result, 'Value', [1, 2])

    __check(result, 'Name', 'foo', 'bar', 'other', 'foo', 'bar')
    __check(result, 'Value', 1, 2, 1, 2, 1)


def test_expand_with_longer_values():
    result = expand([], 'Name', ['foo', 'bar'])
    result = expand(result, 'Value', [1, 2, 3])

    __check(result, 'Name', 'foo', 'bar', 'foo')
    __check(result, 'Value', 1, 2, 3)

    result = expand([], 'Name', ['foo'])
    result = expand(result, 'Value', [1, 2, 3])

    __check(result, 'Name', 'foo', 'foo', 'foo')
    __check(result, 'Value', 1, 2, 3)


def test_expand_with_longer_values_and_repeat():
    result = expand([], 'Name', ['foo', 'bar'])
    result = expand(result, 'Value', [1, 2, 3, 4, 5, 6])

    __check(result, 'Name', 'foo', 'bar', 'foo', 'bar', 'foo', 'bar')
    __check(result, 'Value', 1, 2, 3, 4, 5, 6)

    result = expand([], 'Name', ['foo', 'bar'])
    result = expand(result, 'Value', [1, 2, 3, 4, 5, 6, 7])

    __check(result, 'Name', 'foo', 'bar', 'foo', 'bar', 'foo', 'bar', 'foo')
    __check(result, 'Value', 1, 2, 3, 4, 5, 6, 7)
