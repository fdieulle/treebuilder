import unittest
from treebuilder.expand import expand


class TestExpand(unittest.TestCase):
    def test_with_empty_source(self):
        result = expand([], 'Name', ['foo', 'bar', 'other'])
        
        self.__check(result, 'Name', 'foo', 'bar', 'other')

    def test_with_empty_values(self):
        result = expand([], 'Name', ['foo', 'bar', 'other'])
        result = expand(result, 'Value', [])

        self.__check(result, 'Name', 'foo', 'bar', 'other')
        self.assertTrue(all(['Value' not in x for x in result]))

    def test_expand(self):
        result = expand([], 'Name', ['foo', 'bar', 'other'])
        result = expand(result, 'Value', [1, 2, 3])

        self.__check(result, 'Name', 'foo', 'bar', 'other')
        self.__check(result, 'Value', 1, 2, 3)

    def test_expand_with_smaller_values(self):
        result = expand([], 'Name', ['foo', 'bar', 'other'])
        result = expand(result, 'Value', [1, 2])

        self.__check(result, 'Name', 'foo', 'bar', 'other')
        self.__check(result, 'Value', 1, 2, 1)

        result = expand([], 'Name', ['foo', 'bar', 'other'])
        result = expand(result, 'Value', [1])

        self.__check(result, 'Name', 'foo', 'bar', 'other')
        self.__check(result, 'Value', 1, 1, 1)
        

    def test_expand_with_smaller_values_and_repeat(self):
        result = expand([], 'Name', ['foo', 'bar', 'other', 'foo', 'bar', 'other'])
        result = expand(result, 'Value', [1, 2])

        self.__check(result, 'Name', 'foo', 'bar', 'other', 'foo', 'bar', 'other')
        self.__check(result, 'Value', 1, 2, 1, 2, 1, 2)

        result = expand([], 'Name', ['foo', 'bar', 'other', 'foo', 'bar'])
        result = expand(result, 'Value', [1, 2])

        self.__check(result, 'Name', 'foo', 'bar', 'other', 'foo', 'bar')
        self.__check(result, 'Value', 1, 2, 1, 2, 1)

    
    def test_expand_with_longer_values(self):
        result = expand([], 'Name', ['foo', 'bar'])
        result = expand(result, 'Value', [1, 2, 3])

        self.__check(result, 'Name', 'foo', 'bar', 'foo')
        self.__check(result, 'Value', 1, 2, 3)

        result = expand([], 'Name', ['foo'])
        result = expand(result, 'Value', [1, 2, 3])

        self.__check(result, 'Name', 'foo', 'foo', 'foo')
        self.__check(result, 'Value', 1, 2, 3)

    def test_expand_with_longer_values_and_repear(self):
        result = expand([], 'Name', ['foo', 'bar'])
        result = expand(result, 'Value', [1, 2, 3, 4, 5, 6])

        self.__check(result, 'Name', 'foo', 'bar', 'foo', 'bar', 'foo', 'bar')
        self.__check(result, 'Value', 1, 2, 3, 4, 5, 6)

        result = expand([], 'Name', ['foo', 'bar'])
        result = expand(result, 'Value', [1, 2, 3, 4, 5, 6, 7])

        self.__check(result, 'Name', 'foo', 'bar', 'foo', 'bar', 'foo', 'bar', 'foo')
        self.__check(result, 'Value', 1, 2, 3, 4, 5, 6, 7)

    def __check(self, items, key, *args):
        self.assertListEqual([x[key] for x in items], [x for x in args])


if __name__ == '__main__':
    unittest.main()