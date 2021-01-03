import json
from treebuilder.constants import ATTRIBUTES
import unittest
import os
from treebuilder.TreeBuilder import TreeBuilder


class TestTreeBuilder(unittest.TestCase):
    
    def test_build_simple_tree(self):
        builder = TreeBuilder()

        builder.expand('bookstore/book/title', ['Sapiens', 'Harry Potter', 'A Time of Mercy'])
        builder.set('bookstore/book/is_in_stock', True)
        builder.set('bookstore/book[title="Harry Potter"]/price', 9.99)
        builder.set('bookstore/book[title="A Time of Mercy"]/price', 12.99)
        builder.expand('bookstore/book[title="Sapiens"]/price', [39.99])

        root = builder.root
        self.assertEqual(root['bookstore'][0]['book'][0]['title'], 'Sapiens')
        self.assertEqual(root['bookstore'][0]['book'][0]['is_in_stock'], True)
        self.assertEqual(root['bookstore'][0]['book'][0]['price'], 39.99)

        self.assertEqual(root['bookstore'][0]['book'][1]['title'], 'Harry Potter')
        self.assertEqual(root['bookstore'][0]['book'][1]['is_in_stock'], True)
        self.assertEqual(root['bookstore'][0]['book'][1]['price'], 9.99)
        
        self.assertEqual(root['bookstore'][0]['book'][2]['title'], 'A Time of Mercy')
        self.assertEqual(root['bookstore'][0]['book'][2]['is_in_stock'], True)
        self.assertEqual(root['bookstore'][0]['book'][2]['price'], 12.99)

    def test_bulid_complex_tree(self):
        builder = TreeBuilder()
        builder.expand('Root/Node/Name', ['foo', 'bar'])
        builder.set('Root/Node/@xsi:type', 'MyCustomType')
        builder.cross('Root/Node/Id', [1, 2, 3])
        builder.set('Root/Node[Name=foo]/Details/Description', 'This is foo')
        builder.expand('Root/Node[Name=foo]/Details/Count', ['1', '3'])
        builder.set('Root/Node[Name=bar]/Details/Description', 'This is bar')
        builder.expand('Root/Node[Name=bar]/Details/Count', ['2', '1'])

        builder.set('Root/Node/Details[Count=1]/Value', 10)
        builder.set('Root/Node/Details[Count=2]/Value', 20)
        builder.set('Root/Node/Details[Count=3]/Value', 30)

        root = builder.root
        self.assertEqual(root['Root'][0]['Node'][0]['Name'], 'foo')
        self.assertEqual(root['Root'][0]['Node'][0][ATTRIBUTES]['xsi:type'], 'MyCustomType')
        self.assertEqual(root['Root'][0]['Node'][0]['Id'], 1)
        self.assertEqual(root['Root'][0]['Node'][0]['Details'][0]['Description'], 'This is foo')
        self.assertEqual(root['Root'][0]['Node'][0]['Details'][0]['Count'], '1')
        self.assertEqual(root['Root'][0]['Node'][0]['Details'][0]['Value'], 10)

        self.assertEqual(root['Root'][0]['Node'][1]['Name'], 'bar')
        self.assertEqual(root['Root'][0]['Node'][1][ATTRIBUTES]['xsi:type'], 'MyCustomType')
        self.assertEqual(root['Root'][0]['Node'][1]['Id'], 1)
        self.assertEqual(root['Root'][0]['Node'][1]['Details'][0]['Description'], 'This is bar')
        self.assertEqual(root['Root'][0]['Node'][1]['Details'][0]['Count'], '2')
        self.assertEqual(root['Root'][0]['Node'][1]['Details'][0]['Value'], 20)

        self.assertEqual(root['Root'][0]['Node'][2]['Name'], 'foo')
        self.assertEqual(root['Root'][0]['Node'][2][ATTRIBUTES]['xsi:type'], 'MyCustomType')
        self.assertEqual(root['Root'][0]['Node'][2]['Id'], 2)
        self.assertEqual(root['Root'][0]['Node'][2]['Details'][0]['Description'], 'This is foo')
        self.assertEqual(root['Root'][0]['Node'][2]['Details'][0]['Count'], '3')
        self.assertEqual(root['Root'][0]['Node'][2]['Details'][0]['Value'], 30)

        self.assertEqual(root['Root'][0]['Node'][3]['Name'], 'bar')
        self.assertEqual(root['Root'][0]['Node'][3][ATTRIBUTES]['xsi:type'], 'MyCustomType')
        self.assertEqual(root['Root'][0]['Node'][3]['Id'], 2)
        self.assertEqual(root['Root'][0]['Node'][3]['Details'][0]['Description'], 'This is bar')
        self.assertEqual(root['Root'][0]['Node'][3]['Details'][0]['Count'], '1')
        self.assertEqual(root['Root'][0]['Node'][3]['Details'][0]['Value'], 10)

        self.assertEqual(root['Root'][0]['Node'][4]['Name'], 'foo')
        self.assertEqual(root['Root'][0]['Node'][4][ATTRIBUTES]['xsi:type'], 'MyCustomType')
        self.assertEqual(root['Root'][0]['Node'][4]['Id'], 3)
        self.assertEqual(root['Root'][0]['Node'][4]['Details'][0]['Description'], 'This is foo')
        self.assertEqual(root['Root'][0]['Node'][4]['Details'][0]['Count'], '1')
        self.assertEqual(root['Root'][0]['Node'][4]['Details'][0]['Value'], 10)

        self.assertEqual(root['Root'][0]['Node'][5]['Name'], 'bar')
        self.assertEqual(root['Root'][0]['Node'][5][ATTRIBUTES]['xsi:type'], 'MyCustomType')
        self.assertEqual(root['Root'][0]['Node'][5]['Id'], 3)
        self.assertEqual(root['Root'][0]['Node'][5]['Details'][0]['Description'], 'This is bar')
        self.assertEqual(root['Root'][0]['Node'][5]['Details'][0]['Count'], '2')
        self.assertEqual(root['Root'][0]['Node'][5]['Details'][0]['Value'], 20)

    # def test_to_json(self):
    #     builder = TreeBuilder()

    #     builder.expand('bookstore/books/title', ['Sapiens', 'Harry Potter', 'A Time of Mercy'])
    #     builder.set('bookstore/books/is_in_stock', True)
    #     builder.set('bookstore/books[title="Harry Potter"]/price', 9.99)
    #     builder.set('bookstore/books[title="A Time of Mercy"]/price', 12.99)
    #     builder.expand('bookstore/books[title="Sapiens"]/price', [39.99])
    #     builder.set('bookstore/books/details/count', 3)
    #     builder.set('bookstore/books[title != "Sapiens"]/details/description', 'This is the description')

    #     test_file = 'bookstore.json'
    #     builder.to_json(test_file)

    #     self.__check_files(test_file, self.__get_file_path('bookstore.json'))
    #     # os.remove(test_file)

    # def test_to_xml(self):
    #     builder = TreeBuilder()

    #     builder.set('bookstore/@xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    #     builder.set('bookstore/@xmlns:xsd', 'http://www.w3.org/2001/XMLSchema')
    #     builder.expand('bookstore/book/title', ['Sapiens', 'Harry Potter', 'A Time of Mercy'])
    #     builder.set('bookstore/book/@xsi:type', 'Book')
    #     builder.set('bookstore/book/is_in_stock', True)
    #     builder.set('bookstore/book[title="Harry Potter"]/price', 9.99)
    #     builder.set('bookstore/book[title="A Time of Mercy"]/price', 12.99)
    #     builder.expand('bookstore/book[title="Sapiens"]/price', [39.99])
    #     builder.set('bookstore/book/details/count', 3)
    #     builder.set('bookstore/book[title != "Sapiens"]/details/description', 'This is the description')

    #     test_file = 'bookstore.xml'
    #     builder.to_xml(test_file)

    #     self.__check_files(test_file, self.__get_file_path('bookstore.xml'))
    #     os.remove(test_file)

    def __check_files(self, x: str, y: str):
        with open(x, mode='r') as f:
            x_content = f.read()
        with open(y, mode='r') as f:
            y_content = f.read()
        self.assertEqual(x_content, y_content)
    
    def __get_file_path(self, file_name: str):
        return os.path.join(os.path.dirname(__file__), 'data', file_name)


if __name__ == '__main__':
    unittest.main()