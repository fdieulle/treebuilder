from collections import deque
from itertools import repeat
import json
import xml.etree.ElementTree as ET
from treebuilder.constants import ATTRIBUTES, PARENT
import unittest
import os
from treebuilder.TreeBuilder import TreeBuilder
from treebuilder.xml import to_xml_string


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

    def test_to_json(self):
        builder = TreeBuilder()

        builder.expand('bookstore/books/title', ['Sapiens', 'Harry Potter', 'A Time of Mercy'])
        builder.set('bookstore/books/is_in_stock', True)
        builder.set('bookstore/books[title="Harry Potter"]/price', 9.99)
        builder.set('bookstore/books[title="A Time of Mercy"]/price', 12.99)
        builder.expand('bookstore/books[title="Sapiens"]/price', [39.99])
        builder.set('bookstore/books/details/count', 3)
        builder.set('bookstore/books[title != "Sapiens"]/details/description', 'This is the description')

        test_file = 'bookstore.json'
        builder.to_json(test_file)

        check_file = self.__get_data_file('bookstore.json')
        with open(check_file, mode='r') as f:
            check_data = json.loads(f.read())
        with open(test_file, mode='r') as f:
            test_data = json.loads(f.read())

        stack = deque()
        stack.append((check_data, test_data))
        while len(stack) > 0:
            check_node, test_node = stack.pop()

            if isinstance(check_node, dict):
                self.assertTrue(type(test_node) == dict)
                self.assertTrue(len(check_node) == len(test_node))
                for key in check_node:
                    self.assertTrue(key in test_node)
                    stack.append((check_node[key], test_node[key]))
            elif isinstance(check_node, list):
                self.assertTrue(type(test_node) == list)
                self.assertTrue(len(check_node) == len(test_node))
                [stack.append((c, t)) for c, t in zip(check_node, test_node)]
            else:
                self.assertTrue(check_node == test_node)

        os.remove(test_file)

    def test_to_xml(self):
        builder = TreeBuilder()

        builder.set('bookstore/@xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        builder.set('bookstore/@xmlns:xsd', 'http://www.w3.org/2001/XMLSchema')
        builder.expand('bookstore/book/title', ['Sapiens', 'Harry Potter', 'A Time of Mercy'])
        builder.set('bookstore/book/@xsi:type', 'Book')
        builder.set('bookstore/book/is_in_stock', True)
        builder.set('bookstore/book[title="Harry Potter"]/price', 9.99)
        builder.set('bookstore/book[title="A Time of Mercy"]/price', 12.99)
        builder.expand('bookstore/book[title="Sapiens"]/price', [39.99])
        builder.set('bookstore/book/details/count', 3)
        builder.set('bookstore/book[title != "Sapiens"]/details/description', 'This is the description')

        test_file = 'bookstore.xml'
        builder.to_xml(test_file)

        check_file = self.__get_data_file('bookstore.xml')
        self.__check_xml_files(check_file, test_file)
        
        os.remove(test_file)
    
    def test_doc_example(self):
        
        builder = TreeBuilder()
        # Create 2 books in a bookstore
        builder.expand('/bookstore/book/title', ['Sapiens', 'Harry Potter'])
        # Set the lang to all books
        builder.set('/bookstore/book/@lang', 'en')
        # Set the price to each book
        builder.nest('/bookstore/book/price', [39.95, 29.99])
        # Duplicate each book to make 2 copies
        builder.cross('/bookstore/book/copy_number', [1, 2]) 

        builder.set('/bookstore/book[title=\'Harry Potter\']/author', 'J K. Rowling')
        builder.set('/bookstore/book[title=Sapiens]/author', 'Y N. Harari')

        builder.set('/bookstore/book[title=\'Harry Potter\']/details/published_year', '2005')
        builder.set('/bookstore/book[title=Sapiens]/details/published_year', '2014')

        builder.expand('/bookstore/book[title="Harry Potter"]/borrowers/borrower/name', [f'Client_{i+1}' for i in range(3)])
        builder.expand('/bookstore/book[title=Sapiens]/borrowers/borrower/name', [f'Client_{i+1}' for i in range(5)])

        file_name = 'bookstore_readme.xml'
        builder.to_xml(file_name)

        check_file = self.__get_data_file(file_name)
        self.__check_xml_files(check_file, file_name)

        os.remove(file_name)

    def test_expand_with_attributes(self):
        builder = TreeBuilder()

        builder.expand('Root/Node/Name', ['foo'])
        builder.expand('Root/Node/@value', [1, 2])

        root = builder.root
        self.assertEqual(root['Root'][0]['Node'][0]['Name'], 'foo')
        self.assertEqual(root['Root'][0]['Node'][0][ATTRIBUTES]['value'], 1)
        self.assertEqual(root['Root'][0]['Node'][1]['Name'], 'foo')
        self.assertEqual(root['Root'][0]['Node'][1][ATTRIBUTES]['value'], 2)

    def test_cross_with_attributes(self):
        builder = TreeBuilder()

        builder.expand('Root/Node/Name', ['foo', 'bar'])
        builder.cross('Root/Node/@value', [1, 2])

        root = builder.root
        self.assertEqual(root['Root'][0]['Node'][0]['Name'], 'foo')
        self.assertEqual(root['Root'][0]['Node'][0][ATTRIBUTES]['value'], 1)
        self.assertEqual(root['Root'][0]['Node'][1]['Name'], 'bar')
        self.assertEqual(root['Root'][0]['Node'][1][ATTRIBUTES]['value'], 1)
        self.assertEqual(root['Root'][0]['Node'][2]['Name'], 'foo')
        self.assertEqual(root['Root'][0]['Node'][2][ATTRIBUTES]['value'], 2)
        self.assertEqual(root['Root'][0]['Node'][3]['Name'], 'bar')
        self.assertEqual(root['Root'][0]['Node'][3][ATTRIBUTES]['value'], 2)

    def test_expand_with_attributes_and_filter(self):
        builder = TreeBuilder()

        builder.expand('Root/Node/Name', ['foo', 'bar'])
        builder.expand('Root/Node[Name=foo]/@value', [1, 2])

        root = builder.root
        self.assertEqual(root['Root'][0]['Node'][0]['Name'], 'foo')
        self.assertEqual(root['Root'][0]['Node'][0][ATTRIBUTES]['value'], 1)
        self.assertEqual(root['Root'][0]['Node'][1]['Name'], 'bar')
        self.assertTrue(ATTRIBUTES not in root['Root'][0]['Node'][1])
        self.assertEqual(root['Root'][0]['Node'][2]['Name'], 'foo')
        self.assertEqual(root['Root'][0]['Node'][2][ATTRIBUTES]['value'], 2)

    def test_cross_with_attributes(self):
        builder = TreeBuilder()

        builder.expand('Root/Node/Name', ['foo', 'bar'])
        builder.cross('Root/Node[Name=foo]/@value', [1, 2])

        root = builder.root
        self.assertEqual(root['Root'][0]['Node'][0]['Name'], 'foo')
        self.assertEqual(root['Root'][0]['Node'][0][ATTRIBUTES]['value'], 1)
        self.assertEqual(root['Root'][0]['Node'][1]['Name'], 'bar')
        self.assertTrue(ATTRIBUTES not in root['Root'][0]['Node'][1])
        self.assertEqual(root['Root'][0]['Node'][2]['Name'], 'foo')
        self.assertEqual(root['Root'][0]['Node'][2][ATTRIBUTES]['value'], 2)

    def test_cross_with_sub_node(self):
        builder = TreeBuilder()

        builder.expand('Root/Node/Name', ['foo', 'bar'])
        values = [1, 2]
        
        empty_nodes = [[{}] for v in values]

        builder.cross('Root/Node/SubNode', empty_nodes)
        builder.nest('Root/Node[Name=foo]/SubNode/Value', values)
        builder.nest('Root/Node[Name=bar]/SubNode/Value', values)

        root = builder.root
        self.assertEqual(root['Root'][0]['Node'][0]['Name'], 'foo')
        self.assertEqual(root['Root'][0]['Node'][0]['SubNode'][0]['Value'], 1)
        self.assertEqual(root['Root'][0]['Node'][1]['Name'], 'bar')
        self.assertEqual(root['Root'][0]['Node'][1]['SubNode'][0]['Value'], 1)
        self.assertEqual(root['Root'][0]['Node'][2]['Name'], 'foo')
        self.assertEqual(root['Root'][0]['Node'][2]['SubNode'][0]['Value'], 2)
        self.assertEqual(root['Root'][0]['Node'][3]['Name'], 'bar')
        self.assertEqual(root['Root'][0]['Node'][3]['SubNode'][0]['Value'], 2)

    def test_cross_with_sub_node_and_filter(self):
        builder = TreeBuilder()

        builder.expand('Root/Node/Name', ['foo', 'bar'])
        values = [1, 2]

        builder.cross('Root/Node/SubNode', [[{}] for v in values])
        builder.nest('Root/Node[Name=foo]/SubNode/Value', values)

        root = builder.root
        self.assertEqual(root['Root'][0]['Node'][0]['Name'], 'foo')
        self.assertEqual(root['Root'][0]['Node'][0]['SubNode'][0]['Value'], 1)
        self.assertEqual(root['Root'][0]['Node'][1]['Name'], 'bar')
        self.assertTrue('Value' not in root['Root'][0]['Node'][1]['SubNode'][0])
        self.assertEqual(root['Root'][0]['Node'][2]['Name'], 'foo')
        self.assertEqual(root['Root'][0]['Node'][2]['SubNode'][0]['Value'], 2)
        self.assertEqual(root['Root'][0]['Node'][3]['Name'], 'bar')
        self.assertTrue('Value' not in root['Root'][0]['Node'][3]['SubNode'][0])

        builder.to_xml('test.xml')

    def test_cross_with_sub_node_deeper(self):
        builder = TreeBuilder()

        builder.expand('Root/Node/Name', ['foo', 'bar'])
        values = [1, 2]
        sub_path = 'SubNode1/SubNode2/Value'
        
        split = sub_path.split('/')
        builder.cross(f'Root/Node/{split[0]}', [[{}] for v in values])
        builder.nest(f'Root/Node[Name=foo]/{sub_path}', values)
        builder.nest(f'Root/Node[Name=bar]/{sub_path}', values)

        root = builder.root
        self.assertEqual(root['Root'][0]['Node'][0]['Name'], 'foo')
        self.assertEqual(root['Root'][0]['Node'][0]['SubNode1'][0]['SubNode2'][0]['Value'], 1)
        self.assertEqual(root['Root'][0]['Node'][1]['Name'], 'bar')
        self.assertEqual(root['Root'][0]['Node'][1]['SubNode1'][0]['SubNode2'][0]['Value'], 1)
        self.assertEqual(root['Root'][0]['Node'][2]['Name'], 'foo')
        self.assertEqual(root['Root'][0]['Node'][2]['SubNode1'][0]['SubNode2'][0]['Value'], 2)
        self.assertEqual(root['Root'][0]['Node'][3]['Name'], 'bar')
        self.assertEqual(root['Root'][0]['Node'][3]['SubNode1'][0]['SubNode2'][0]['Value'], 2)

    def test_get_items(self):
        builder = TreeBuilder()

        builder.expand('/bookstore/book/title', ['Sapiens', 'Harry Potter'])
        builder.set('/bookstore/book/@lang', 'en')
        builder.nest('/bookstore/book/price', [39.95, 29.99])
        builder.cross('/bookstore/book/copy_number', ['1', '2']) 

        titles = builder.get_items('/bookstore/book/title')
        self.assertTrue(titles == ['Sapiens', 'Harry Potter', 'Sapiens', 'Harry Potter'])

        langs = builder.get_items('/bookstore/book/@lang')
        self.assertTrue(langs == [x for x in repeat('en', 4)])

        books = builder.get_items('/bookstore/book')[0]
        self.assertTrue(len(books) == 4)

        copy_numbers = [x['copy_number'] for x in books]
        self.assertTrue(copy_numbers == ['1', '1', '2', '2'])

        titles = builder.get_items('/bookstore/book[copy_number=2]/title')
        self.assertTrue(titles == ['Sapiens', 'Harry Potter'])

    def test_expand_from_ancestor(self):
        builder = TreeBuilder()

        builder.expand('/bookstore/book/title', ['Sapiens', 'Harry Potter'])
        builder.expand('/bookstore/book/details/copy_number', [1, 2, 3], from_ancestor='book')

        root = builder.root
        self.assertEqual(root['bookstore'][0]['book'][0]['title'], 'Sapiens')
        self.assertEqual(root['bookstore'][0]['book'][0]['details'][0]['copy_number'], 1)
        self.assertEqual(root['bookstore'][0]['book'][1]['title'], 'Harry Potter')
        self.assertEqual(root['bookstore'][0]['book'][1]['details'][0]['copy_number'], 2)
        self.assertEqual(root['bookstore'][0]['book'][2]['title'], 'Sapiens')
        self.assertEqual(root['bookstore'][0]['book'][2]['details'][0]['copy_number'], 3)
        self.assertTrue(len(root['bookstore'][0]['book']) == 3)

    def test_expand_from_ancestor_with_an_existing_sub_tree(self):
        builder = TreeBuilder()

        builder.expand('/bookstore/book/title', ['Sapiens', 'Harry Potter'])
        builder.expand('/bookstore/book/price', [39.95, 29.99])
        builder.expand('/bookstore/book/details/published_year', [2014, 2005])
        builder.expand('/bookstore/book/details/copy_number', [1, 1, 2, 2], from_ancestor='book')

        root = builder.root
        self.assertEqual(root['bookstore'][0]['book'][0]['title'], 'Sapiens')
        self.assertEqual(root['bookstore'][0]['book'][0]['price'], 39.95)
        self.assertEqual(root['bookstore'][0]['book'][0]['details'][0]['published_year'], 2014)
        self.assertEqual(root['bookstore'][0]['book'][0]['details'][0]['copy_number'], 1)
        self.assertEqual(root['bookstore'][0]['book'][1]['title'], 'Harry Potter')
        self.assertEqual(root['bookstore'][0]['book'][1]['price'], 29.99)
        self.assertEqual(root['bookstore'][0]['book'][1]['details'][0]['published_year'], 2005)
        self.assertEqual(root['bookstore'][0]['book'][1]['details'][0]['copy_number'], 1)
        self.assertEqual(root['bookstore'][0]['book'][2]['title'], 'Sapiens')
        self.assertEqual(root['bookstore'][0]['book'][2]['price'], 39.95)
        self.assertEqual(root['bookstore'][0]['book'][2]['details'][0]['published_year'], 2014)
        self.assertEqual(root['bookstore'][0]['book'][2]['details'][0]['copy_number'], 2)
        self.assertEqual(root['bookstore'][0]['book'][3]['title'], 'Harry Potter')
        self.assertEqual(root['bookstore'][0]['book'][3]['price'], 29.99)
        self.assertEqual(root['bookstore'][0]['book'][3]['details'][0]['published_year'], 2005)
        self.assertEqual(root['bookstore'][0]['book'][3]['details'][0]['copy_number'], 2)
        self.assertTrue(len(root['bookstore'][0]['book']) == 4)

    def test_cross_from_ancestor(self):
        builder = TreeBuilder()

        builder.expand('/bookstore/book/title', ['Sapiens', 'Harry Potter'])
        builder.cross('/bookstore/book/details/copy_number', [1, 2, 3], from_ancestor='book')

        root = builder.root
        self.assertEqual(root['bookstore'][0]['book'][0]['title'], 'Sapiens')
        self.assertEqual(root['bookstore'][0]['book'][0]['details'][0]['copy_number'], 1)
        self.assertEqual(root['bookstore'][0]['book'][1]['title'], 'Harry Potter')
        self.assertEqual(root['bookstore'][0]['book'][1]['details'][0]['copy_number'], 1)
        self.assertEqual(root['bookstore'][0]['book'][2]['title'], 'Sapiens')
        self.assertEqual(root['bookstore'][0]['book'][2]['details'][0]['copy_number'], 2)
        self.assertEqual(root['bookstore'][0]['book'][3]['title'], 'Harry Potter')
        self.assertEqual(root['bookstore'][0]['book'][3]['details'][0]['copy_number'], 2)
        self.assertEqual(root['bookstore'][0]['book'][4]['title'], 'Sapiens')
        self.assertEqual(root['bookstore'][0]['book'][4]['details'][0]['copy_number'], 3)
        self.assertEqual(root['bookstore'][0]['book'][5]['title'], 'Harry Potter')
        self.assertEqual(root['bookstore'][0]['book'][5]['details'][0]['copy_number'], 3)
        self.assertTrue(len(root['bookstore'][0]['book']) == 6)

    def test_cross_from_ancestor_with_an_existing_sub_tree(self):
        builder = TreeBuilder()

        builder.expand('/bookstore/book/title', ['Sapiens', 'Harry Potter'])
        builder.expand('/bookstore/book/price', [39.95, 29.99])
        builder.expand('/bookstore/book/details/published_year', [2014, 2005])
        builder.cross('/bookstore/book/details/copy_number', [1, 2], from_ancestor='book')

        root = builder.root
        self.assertEqual(root['bookstore'][0]['book'][0]['title'], 'Sapiens')
        self.assertEqual(root['bookstore'][0]['book'][0]['price'], 39.95)
        self.assertEqual(root['bookstore'][0]['book'][0]['details'][0]['published_year'], 2014)
        self.assertEqual(root['bookstore'][0]['book'][0]['details'][0]['copy_number'], 1)
        self.assertEqual(root['bookstore'][0]['book'][1]['title'], 'Harry Potter')
        self.assertEqual(root['bookstore'][0]['book'][1]['price'], 29.99)
        self.assertEqual(root['bookstore'][0]['book'][1]['details'][0]['published_year'], 2005)
        self.assertEqual(root['bookstore'][0]['book'][1]['details'][0]['copy_number'], 1)
        self.assertEqual(root['bookstore'][0]['book'][2]['title'], 'Sapiens')
        self.assertEqual(root['bookstore'][0]['book'][2]['price'], 39.95)
        self.assertEqual(root['bookstore'][0]['book'][2]['details'][0]['published_year'], 2014)
        self.assertEqual(root['bookstore'][0]['book'][2]['details'][0]['copy_number'], 2)
        self.assertEqual(root['bookstore'][0]['book'][3]['title'], 'Harry Potter')
        self.assertEqual(root['bookstore'][0]['book'][3]['price'], 29.99)
        self.assertEqual(root['bookstore'][0]['book'][3]['details'][0]['published_year'], 2005)
        self.assertEqual(root['bookstore'][0]['book'][3]['details'][0]['copy_number'], 2)
        self.assertTrue(len(root['bookstore'][0]['book']) == 4)


    def __check_xml_files(self, x_file, y_file):
        x_xml = ET.parse(x_file)
        y_xml = ET.parse(y_file)

        stack = deque()
        stack.append((x_xml.getroot(), y_xml.getroot()))
        while len(stack) > 0:
            x_node, y_node = stack.pop()

            self.assertTrue(len(x_node) == len(y_node))
            
            # Check attributes
            if x_node.attrib is not None:
                self.assertTrue(len(x_node.attrib) == len(y_node.attrib))
                for key in x_node.attrib:
                    self.assertTrue(x_node.attrib[key] == y_node.attrib[key])
            else:
                self.assertTrue(y_node.attrib is None)
            
            if len(x_node) == 0:
                self.assertTrue(x_node.text == y_node.text)
            else:
                [stack.append((c, t)) for c, t in zip(x_node, y_node)]

    def __get_data_file(self, file_name: str):
        return os.path.join(os.path.dirname(__file__), 'data', file_name)


if __name__ == '__main__':
    unittest.main()