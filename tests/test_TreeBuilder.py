from collections import deque
from itertools import repeat
import json
import xml.etree.ElementTree as ET
from treebuilder.constants import ATTRIBUTES
import os
from treebuilder.TreeBuilder import TreeBuilder
from treebuilder.xml import to_xml_string


def __check_xml_files(x_file, y_file):
    x_xml = ET.parse(x_file)
    y_xml = ET.parse(y_file)

    stack = deque()
    stack.append((x_xml.getroot(), y_xml.getroot()))
    while len(stack) > 0:
        x_node, y_node = stack.pop()

        assert len(x_node) == len(y_node)
        
        # Check attributes
        if x_node.attrib is not None:
            assert len(x_node.attrib) == len(y_node.attrib)
            for key in x_node.attrib:
                assert x_node.attrib[key] == y_node.attrib[key]
        else:
            assert y_node.attrib is None
        
        if len(x_node) == 0:
            assert x_node.text == y_node.text
        else:
            [stack.append((c, t)) for c, t in zip(x_node, y_node)]


def __get_data_file(file_name: str):
    return os.path.join(os.path.dirname(__file__), 'data', file_name)


def test_build_simple_tree():
    builder = TreeBuilder()

    builder.expand('bookstore/book/title', ['Sapiens', 'Harry Potter', 'A Time of Mercy'])
    builder.set('bookstore/book/is_in_stock', True)
    builder.set('bookstore/book[title="Harry Potter"]/price', 9.99)
    builder.set('bookstore/book[title="A Time of Mercy"]/price', 12.99)
    builder.expand('bookstore/book[title="Sapiens"]/price', [39.99])

    root = builder.root
    assert root['bookstore'][0]['book'][0]['title'] == 'Sapiens'
    assert root['bookstore'][0]['book'][0]['is_in_stock'] == True
    assert root['bookstore'][0]['book'][0]['price'] == 39.99

    assert root['bookstore'][0]['book'][1]['title'] == 'Harry Potter'
    assert root['bookstore'][0]['book'][1]['is_in_stock'] == True
    assert root['bookstore'][0]['book'][1]['price'] == 9.99
    
    assert root['bookstore'][0]['book'][2]['title'] == 'A Time of Mercy'
    assert root['bookstore'][0]['book'][2]['is_in_stock'] == True
    assert root['bookstore'][0]['book'][2]['price'] == 12.99


def test_bulid_complex_tree():
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
    assert root['Root'][0]['Node'][0]['Name'] == 'foo'
    assert root['Root'][0]['Node'][0][ATTRIBUTES]['xsi:type'] == 'MyCustomType'
    assert root['Root'][0]['Node'][0]['Id'] == 1
    assert root['Root'][0]['Node'][0]['Details'][0]['Description'] == 'This is foo'
    assert root['Root'][0]['Node'][0]['Details'][0]['Count'] == '1'
    assert root['Root'][0]['Node'][0]['Details'][0]['Value'] == 10

    assert root['Root'][0]['Node'][1]['Name'] == 'bar'
    assert root['Root'][0]['Node'][1][ATTRIBUTES]['xsi:type'] ==  'MyCustomType'
    assert root['Root'][0]['Node'][1]['Id'] ==  1
    assert root['Root'][0]['Node'][1]['Details'][0]['Description'] ==  'This is bar'
    assert root['Root'][0]['Node'][1]['Details'][0]['Count'] ==  '2'
    assert root['Root'][0]['Node'][1]['Details'][0]['Value'] ==  20

    assert root['Root'][0]['Node'][2]['Name'] ==  'foo'
    assert root['Root'][0]['Node'][2][ATTRIBUTES]['xsi:type'] ==  'MyCustomType'
    assert root['Root'][0]['Node'][2]['Id'] ==  2
    assert root['Root'][0]['Node'][2]['Details'][0]['Description'] ==  'This is foo'
    assert root['Root'][0]['Node'][2]['Details'][0]['Count'] ==  '3'
    assert root['Root'][0]['Node'][2]['Details'][0]['Value'] ==  30

    assert root['Root'][0]['Node'][3]['Name'] ==  'bar'
    assert root['Root'][0]['Node'][3][ATTRIBUTES]['xsi:type'], 'MyCustomType'
    assert root['Root'][0]['Node'][3]['Id'] ==  2
    assert root['Root'][0]['Node'][3]['Details'][0]['Description'] ==  'This is bar'
    assert root['Root'][0]['Node'][3]['Details'][0]['Count'] ==  '1'
    assert root['Root'][0]['Node'][3]['Details'][0]['Value'] ==  10

    assert root['Root'][0]['Node'][4]['Name'] ==  'foo'
    assert root['Root'][0]['Node'][4][ATTRIBUTES]['xsi:type'] ==  'MyCustomType'
    assert root['Root'][0]['Node'][4]['Id'] ==  3
    assert root['Root'][0]['Node'][4]['Details'][0]['Description'] ==  'This is foo'
    assert root['Root'][0]['Node'][4]['Details'][0]['Count'] ==  '1'
    assert root['Root'][0]['Node'][4]['Details'][0]['Value'] ==  10

    assert root['Root'][0]['Node'][5]['Name'] ==  'bar'
    assert root['Root'][0]['Node'][5][ATTRIBUTES]['xsi:type'] ==  'MyCustomType'
    assert root['Root'][0]['Node'][5]['Id'] ==  3
    assert root['Root'][0]['Node'][5]['Details'][0]['Description'] ==  'This is bar'
    assert root['Root'][0]['Node'][5]['Details'][0]['Count'] ==  '2'
    assert root['Root'][0]['Node'][5]['Details'][0]['Value'] ==  20


def test_to_json(tmpdir):
    builder = TreeBuilder()

    builder.expand('bookstore/books/title', ['Sapiens', 'Harry Potter', 'A Time of Mercy'])
    builder.set('bookstore/books/is_in_stock', True)
    builder.set('bookstore/books[title="Harry Potter"]/price', 9.99)
    builder.set('bookstore/books[title="A Time of Mercy"]/price', 12.99)
    builder.expand('bookstore/books[title="Sapiens"]/price', [39.99])
    builder.set('bookstore/books/details/count', 3)
    builder.set('bookstore/books[title != "Sapiens"]/details/description', 'This is the description')

    test_file = os.path.join(tmpdir, 'bookstore.json')
    builder.to_json(test_file)

    check_file = __get_data_file('bookstore.json')
    with open(check_file, mode='r') as f:
        check_data = json.loads(f.read())
    with open(test_file, mode='r') as f:
        test_data = json.loads(f.read())

    stack = deque()
    stack.append((check_data, test_data))
    while len(stack) > 0:
        check_node, test_node = stack.pop()

        if isinstance(check_node, dict):
            assert type(test_node) == dict
            assert len(check_node) == len(test_node)
            for key in check_node:
                assert key in test_node
                stack.append((check_node[key], test_node[key]))
        elif isinstance(check_node, list):
            assert type(test_node) == list
            assert len(check_node) == len(test_node)
            [stack.append((c, t)) for c, t in zip(check_node, test_node)]
        else:
            assert check_node == test_node


def test_to_xml(tmpdir):
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

    test_file = os.path.join(tmpdir, 'bookstore.xml')
    builder.to_xml(test_file)

    check_file = __get_data_file('bookstore.xml')
    __check_xml_files(check_file, test_file)


def test_doc_example(tmpdir):
    
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

    test_file = os.path.join(tmpdir, 'bookstore_readme.xml')
    builder.to_xml(test_file)

    check_file = __get_data_file('bookstore_readme.xml')
    __check_xml_files(check_file, test_file)


def test_expand_with_attributes():
    builder = TreeBuilder()

    builder.expand('Root/Node/Name', ['foo'])
    builder.expand('Root/Node/@value', [1, 2])

    root = builder.root
    assert root['Root'][0]['Node'][0]['Name'] == 'foo'
    assert root['Root'][0]['Node'][0][ATTRIBUTES]['value'] == 1
    assert root['Root'][0]['Node'][1]['Name'] == 'foo'
    assert root['Root'][0]['Node'][1][ATTRIBUTES]['value'] == 2


def test_cross_with_attributes():
    builder = TreeBuilder()

    builder.expand('Root/Node/Name', ['foo', 'bar'])
    builder.cross('Root/Node/@value', [1, 2])

    root = builder.root
    assert root['Root'][0]['Node'][0]['Name'] == 'foo'
    assert root['Root'][0]['Node'][0][ATTRIBUTES]['value'] == 1
    assert root['Root'][0]['Node'][1]['Name'] == 'bar'
    assert root['Root'][0]['Node'][1][ATTRIBUTES]['value'] == 1
    assert root['Root'][0]['Node'][2]['Name'] == 'foo'
    assert root['Root'][0]['Node'][2][ATTRIBUTES]['value'] == 2
    assert root['Root'][0]['Node'][3]['Name'] == 'bar'
    assert root['Root'][0]['Node'][3][ATTRIBUTES]['value'] == 2


def test_expand_with_attributes_and_filter():
    builder = TreeBuilder()

    builder.expand('Root/Node/Name', ['foo', 'bar'])
    builder.expand('Root/Node[Name=foo]/@value', [1, 2])

    root = builder.root
    assert root['Root'][0]['Node'][0]['Name'] == 'foo'
    assert root['Root'][0]['Node'][0][ATTRIBUTES]['value'] == 1
    assert root['Root'][0]['Node'][1]['Name'] == 'bar'
    assert ATTRIBUTES not in root['Root'][0]['Node'][1]
    assert root['Root'][0]['Node'][2]['Name'] == 'foo'
    assert root['Root'][0]['Node'][2][ATTRIBUTES]['value'] == 2


def test_cross_with_attributes():
    builder = TreeBuilder()

    builder.expand('Root/Node/Name', ['foo', 'bar'])
    builder.cross('Root/Node[Name=foo]/@value', [1, 2])

    root = builder.root
    assert root['Root'][0]['Node'][0]['Name'] == 'foo'
    assert root['Root'][0]['Node'][0][ATTRIBUTES]['value'] == 1
    assert root['Root'][0]['Node'][1]['Name'] == 'bar'
    assert ATTRIBUTES not in root['Root'][0]['Node'][1]
    assert root['Root'][0]['Node'][2]['Name'] == 'foo'
    assert root['Root'][0]['Node'][2][ATTRIBUTES]['value'] == 2


def test_cross_with_sub_node():
    builder = TreeBuilder()

    builder.expand('Root/Node/Name', ['foo', 'bar'])
    values = [1, 2]
    
    empty_nodes = [[{}] for v in values]

    builder.cross('Root/Node/SubNode', empty_nodes)
    builder.nest('Root/Node[Name=foo]/SubNode/Value', values)
    builder.nest('Root/Node[Name=bar]/SubNode/Value', values)

    root = builder.root
    assert root['Root'][0]['Node'][0]['Name'] == 'foo'
    assert root['Root'][0]['Node'][0]['SubNode'][0]['Value'] == 1
    assert root['Root'][0]['Node'][1]['Name'] == 'bar'
    assert root['Root'][0]['Node'][1]['SubNode'][0]['Value'] == 1
    assert root['Root'][0]['Node'][2]['Name'] == 'foo'
    assert root['Root'][0]['Node'][2]['SubNode'][0]['Value'] == 2
    assert root['Root'][0]['Node'][3]['Name'] == 'bar'
    assert root['Root'][0]['Node'][3]['SubNode'][0]['Value'] == 2


def test_cross_with_sub_node_and_filter():
    builder = TreeBuilder()

    builder.expand('Root/Node/Name', ['foo', 'bar'])
    values = [1, 2]

    builder.cross('Root/Node/SubNode', [[{}] for v in values])
    builder.nest('Root/Node[Name=foo]/SubNode/Value', values)

    root = builder.root
    assert root['Root'][0]['Node'][0]['Name'] == 'foo'
    assert root['Root'][0]['Node'][0]['SubNode'][0]['Value'] == 1
    assert root['Root'][0]['Node'][1]['Name'] == 'bar'
    assert 'Value' not in root['Root'][0]['Node'][1]['SubNode'][0]
    assert root['Root'][0]['Node'][2]['Name'] == 'foo'
    assert root['Root'][0]['Node'][2]['SubNode'][0]['Value'] == 2
    assert root['Root'][0]['Node'][3]['Name'] == 'bar'
    assert 'Value' not in root['Root'][0]['Node'][3]['SubNode'][0]


def test_cross_with_sub_node_deeper():
    builder = TreeBuilder()

    builder.expand('Root/Node/Name', ['foo', 'bar'])
    values = [1, 2]
    sub_path = 'SubNode1/SubNode2/Value'
    
    split = sub_path.split('/')
    builder.cross(f'Root/Node/{split[0]}', [[{}] for v in values])
    builder.nest(f'Root/Node[Name=foo]/{sub_path}', values)
    builder.nest(f'Root/Node[Name=bar]/{sub_path}', values)

    root = builder.root
    assert root['Root'][0]['Node'][0]['Name'] == 'foo'
    assert root['Root'][0]['Node'][0]['SubNode1'][0]['SubNode2'][0]['Value'] == 1
    assert root['Root'][0]['Node'][1]['Name'] == 'bar'
    assert root['Root'][0]['Node'][1]['SubNode1'][0]['SubNode2'][0]['Value'] == 1
    assert root['Root'][0]['Node'][2]['Name'] == 'foo'
    assert root['Root'][0]['Node'][2]['SubNode1'][0]['SubNode2'][0]['Value'] == 2
    assert root['Root'][0]['Node'][3]['Name'] == 'bar'
    assert root['Root'][0]['Node'][3]['SubNode1'][0]['SubNode2'][0]['Value'] == 2


def test_get_items():
    builder = TreeBuilder()

    builder.expand('/bookstore/book/title', ['Sapiens', 'Harry Potter'])
    builder.set('/bookstore/book/@lang', 'en')
    builder.nest('/bookstore/book/price', ['$39.95', '$29.99'])
    builder.cross('/bookstore/book/details/copy_number', ['1', '2'], from_ancestor='book') 

    titles = builder.get_items('/bookstore/book/title')
    assert titles == ['Sapiens', 'Harry Potter', 'Sapiens', 'Harry Potter']

    langs = builder.get_items('/bookstore/book/@lang')
    assert langs == [x for x in repeat('en', 4)]

    books = builder.get_items('/bookstore/book')
    assert len(books) == 4

    prices = [x['price'] for x in books]
    assert prices == ['$39.95', '$29.99', '$39.95', '$29.99']

    titles = builder.get_items('/bookstore/book[price="$29.99"]/title')
    assert titles == ['Harry Potter', 'Harry Potter']

    details = builder.get_items('/bookstore/book[price="$29.99"]/details')
    copy_numbers = [x['copy_number'] for x in details]
    assert copy_numbers == ['1', '2']


def test_expand_from_ancestor():
    builder = TreeBuilder()

    builder.expand('/bookstore/book/title', ['Sapiens', 'Harry Potter'])
    builder.expand('/bookstore/book/details/copy_number', [1, 2, 3], from_ancestor='book')

    root = builder.root
    assert root['bookstore'][0]['book'][0]['title'], 'Sapiens'
    assert root['bookstore'][0]['book'][0]['details'][0]['copy_number'], 1
    assert root['bookstore'][0]['book'][1]['title'], 'Harry Potter'
    assert root['bookstore'][0]['book'][1]['details'][0]['copy_number'], 2
    assert root['bookstore'][0]['book'][2]['title'], 'Sapiens'
    assert root['bookstore'][0]['book'][2]['details'][0]['copy_number'], 3
    assert len(root['bookstore'][0]['book']) == 3


def test_expand_from_ancestor_without_expansion():
    builder = TreeBuilder()

    builder.expand('/bookstore/book/title', ['Sapiens', 'Harry Potter'])
    builder.expand('/bookstore/book/details/copy_number', [1], from_ancestor='book')

    root = builder.root
    assert root['bookstore'][0]['book'][0]['title'], 'Sapiens'
    assert root['bookstore'][0]['book'][0]['details'][0]['copy_number'], 1
    assert root['bookstore'][0]['book'][1]['title'], 'Harry Potter'
    assert root['bookstore'][0]['book'][1]['details'][0]['copy_number'], 1
    assert len(root['bookstore'][0]['book']) == 2

def test_expand_from_ancestor_with_an_existing_sub_tree():
    builder = TreeBuilder()

    builder.expand('/bookstore/book/title', ['Sapiens', 'Harry Potter'])
    builder.expand('/bookstore/book/price', [39.95, 29.99])
    builder.expand('/bookstore/book/details/published_year', [2014, 2005])
    builder.expand('/bookstore/book/details/copy_number', [1, 1, 2, 2], from_ancestor='book')

    root = builder.root
    assert root['bookstore'][0]['book'][0]['title'] == 'Sapiens'
    assert root['bookstore'][0]['book'][0]['price'] == 39.95
    assert root['bookstore'][0]['book'][0]['details'][0]['published_year'] == 2014
    assert root['bookstore'][0]['book'][0]['details'][0]['copy_number'] == 1
    assert root['bookstore'][0]['book'][1]['title'] == 'Harry Potter'
    assert root['bookstore'][0]['book'][1]['price'] == 29.99
    assert root['bookstore'][0]['book'][1]['details'][0]['published_year'] == 2005
    assert root['bookstore'][0]['book'][1]['details'][0]['copy_number'] == 1
    assert root['bookstore'][0]['book'][2]['title'] == 'Sapiens'
    assert root['bookstore'][0]['book'][2]['price'] == 39.95
    assert root['bookstore'][0]['book'][2]['details'][0]['published_year'] == 2014
    assert root['bookstore'][0]['book'][2]['details'][0]['copy_number'] == 2
    assert root['bookstore'][0]['book'][3]['title'] == 'Harry Potter'
    assert root['bookstore'][0]['book'][3]['price'] == 29.99
    assert root['bookstore'][0]['book'][3]['details'][0]['published_year'] == 2005
    assert root['bookstore'][0]['book'][3]['details'][0]['copy_number'] == 2
    assert len(root['bookstore'][0]['book']) == 4


def test_cross_from_ancestor():
    builder = TreeBuilder()

    builder.expand('/bookstore/book/title', ['Sapiens', 'Harry Potter'])
    builder.cross('/bookstore/book/details/copy_number', [1, 2, 3], from_ancestor='book')

    root = builder.root
    assert root['bookstore'][0]['book'][0]['title'] == 'Sapiens'
    assert root['bookstore'][0]['book'][0]['details'][0]['copy_number'] == 1
    assert root['bookstore'][0]['book'][1]['title'] == 'Harry Potter'
    assert root['bookstore'][0]['book'][1]['details'][0]['copy_number'] == 1
    assert root['bookstore'][0]['book'][2]['title'] == 'Sapiens'
    assert root['bookstore'][0]['book'][2]['details'][0]['copy_number'] == 2
    assert root['bookstore'][0]['book'][3]['title'] == 'Harry Potter'
    assert root['bookstore'][0]['book'][3]['details'][0]['copy_number'] == 2
    assert root['bookstore'][0]['book'][4]['title'] == 'Sapiens'
    assert root['bookstore'][0]['book'][4]['details'][0]['copy_number'] == 3
    assert root['bookstore'][0]['book'][5]['title'] == 'Harry Potter'
    assert root['bookstore'][0]['book'][5]['details'][0]['copy_number'] == 3
    assert len(root['bookstore'][0]['book']) == 6


def test_cross_from_ancestor_with_an_existing_sub_tree():
    builder = TreeBuilder()

    builder.expand('/bookstore/book/title', ['Sapiens', 'Harry Potter'])
    builder.expand('/bookstore/book/price', [39.95, 29.99])
    builder.expand('/bookstore/book/details/published_year', [2014, 2005])
    builder.cross('/bookstore/book/details/copy_number', [1, 2], from_ancestor='book')

    root = builder.root
    assert root['bookstore'][0]['book'][0]['title'] == 'Sapiens'
    assert root['bookstore'][0]['book'][0]['price'] == 39.95
    assert root['bookstore'][0]['book'][0]['details'][0]['published_year'] == 2014
    assert root['bookstore'][0]['book'][0]['details'][0]['copy_number'] == 1
    assert root['bookstore'][0]['book'][1]['title'] == 'Harry Potter'
    assert root['bookstore'][0]['book'][1]['price'] == 29.99
    assert root['bookstore'][0]['book'][1]['details'][0]['published_year'] == 2005
    assert root['bookstore'][0]['book'][1]['details'][0]['copy_number'] == 1
    assert root['bookstore'][0]['book'][2]['title'] == 'Sapiens'
    assert root['bookstore'][0]['book'][2]['price'] == 39.95
    assert root['bookstore'][0]['book'][2]['details'][0]['published_year'] == 2014
    assert root['bookstore'][0]['book'][2]['details'][0]['copy_number'] == 2
    assert root['bookstore'][0]['book'][3]['title'] == 'Harry Potter'
    assert root['bookstore'][0]['book'][3]['price'] == 29.99
    assert root['bookstore'][0]['book'][3]['details'][0]['published_year'] == 2005
    assert root['bookstore'][0]['book'][3]['details'][0]['copy_number'] == 2
    assert len(root['bookstore'][0]['book']) == 4


def test_node_deep_copy_with_expand():
    builder = TreeBuilder()

    builder.expand('bookstore/book/details/@lang', ['en'])
    builder.expand('bookstore/book/title', ['Sapiens', 'Harry Potter'])
    builder.expand('bookstore/book/details/published_year', [2014, 2005])
    builder.expand('bookstore/book/details/copy_number', [1, 2])

    root = builder.root
    assert root['bookstore'][0]['book'][0]['title'] == 'Sapiens'
    assert root['bookstore'][0]['book'][0]['details'][0][ATTRIBUTES]['lang'] == 'en'
    assert root['bookstore'][0]['book'][0]['details'][0]['published_year'] == 2014
    assert root['bookstore'][0]['book'][0]['details'][0]['copy_number'] == 1
    assert root['bookstore'][0]['book'][1]['title'] == 'Harry Potter'
    assert root['bookstore'][0]['book'][1]['details'][0][ATTRIBUTES]['lang'] == 'en'
    assert root['bookstore'][0]['book'][1]['details'][0]['published_year'] == 2005
    assert root['bookstore'][0]['book'][1]['details'][0]['copy_number'] == 2
    assert len(root['bookstore'][0]['book']) == 2


def test_node_deep_copy_with_cross():
    builder = TreeBuilder()

    builder.expand('bookstore/book/details/@lang', ['en'])
    builder.cross('bookstore/book/title', ['Sapiens', 'Harry Potter'])
    builder.expand('bookstore/book/details/published_year', [2014, 2005])
    builder.expand('bookstore/book/details/copy_number', [1, 2])

    root = builder.root
    assert root['bookstore'][0]['book'][0]['title'] == 'Sapiens'
    assert root['bookstore'][0]['book'][0]['details'][0][ATTRIBUTES]['lang'] == 'en'
    assert root['bookstore'][0]['book'][0]['details'][0]['published_year'] == 2014
    assert root['bookstore'][0]['book'][0]['details'][0]['copy_number'] == 1
    assert root['bookstore'][0]['book'][1]['title'] == 'Harry Potter'
    assert root['bookstore'][0]['book'][1]['details'][0][ATTRIBUTES]['lang'] == 'en'
    assert root['bookstore'][0]['book'][1]['details'][0]['published_year'] == 2005
    assert root['bookstore'][0]['book'][1]['details'][0]['copy_number'] == 2
    assert len(root['bookstore'][0]['book']) == 2
