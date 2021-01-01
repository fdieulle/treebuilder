import unittest
from treebuilder.cross import cross
from treebuilder.expand import expand


class TestCross(unittest.TestCase):
    def test_with_empty_source(self):
        result = cross([], 'Name', ['foo', 'bar', 'other'])
        
        self.__check(result, 'Name', 'foo', 'bar', 'other')

    def test_with_empty_values(self):
        result = expand([], 'Name', ['foo', 'bar', 'other'])
        result = cross(result, 'Value', [])

        self.assertTrue(len(result) == 0) # Because N x 0 = 0

    def test_cross(self):
        result = expand([], 'Name', ['foo', 'bar', 'other'])
        result = cross(result, 'Value', [1, 2, 3])

        self.__check(result, 'Name', 'foo', 'bar', 'other', 'foo', 'bar', 'other', 'foo', 'bar', 'other')
        self.__check(result, 'Value', 1, 1, 1, 2, 2, 2, 3, 3, 3)

    def test_cross_with_smaller_values(self):
        result = expand([], 'Name', ['foo', 'bar', 'other'])
        result = cross(result, 'Value', [1, 2])

        self.__check(result, 'Name', 'foo', 'bar', 'other', 'foo', 'bar', 'other')
        self.__check(result, 'Value', 1, 1, 1, 2, 2, 2)

        result = expand([], 'Name', ['foo', 'bar', 'other'])
        result = cross(result, 'Value', [1])

        self.__check(result, 'Name', 'foo', 'bar', 'other')
        self.__check(result, 'Value', 1, 1, 1)

    
    def test_cross_with_longer_values(self):
        result = expand([], 'Name', ['foo', 'bar'])
        result = cross(result, 'Value', [1, 2, 3])

        self.__check(result, 'Name', 'foo', 'bar', 'foo', 'bar', 'foo', 'bar')
        self.__check(result, 'Value', 1, 1, 2, 2, 3, 3)

        result = expand([], 'Name', ['foo'])
        result = cross(result, 'Value', [1, 2, 3])

        self.__check(result, 'Name', 'foo', 'foo', 'foo')
        self.__check(result, 'Value', 1, 2, 3)

    def __check(self, items, key, *args):
        self.assertListEqual([x[key] for x in items], [x for x in args])


if __name__ == '__main__':
    unittest.main()