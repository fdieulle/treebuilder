from typing import Any, Dict, List, Tuple
from collections import deque
from itertools import compress

from treebuilder.constants import ATTRIBUTES, PARENT
from treebuilder.FilterLexer import FilterLexer
from treebuilder.FilterParser import FilterParser
from treebuilder.expand import expand
from treebuilder.cross import cross
from treebuilder.nest import nest
from treebuilder.xml import to_xml
from treebuilder.json import to_json


class TreeBuilder:
    """Tree bulider main class.
    """
    @property
    def root(self):
        """[Dict[str, Any]]: Gets the tree root."""
        return self.__root

    def __init__(self):
        self.__root = {}
        self.__lexer = FilterLexer()
        self.__parser = FilterParser()

    def set(self, xpath: str, value: Any) -> 'TreeBuilder':
        """Set value for a tree sub set

        Args:
            xpath: (str): The xpath to extract tree sub set
            value: (Any): The value to apply for each leaf found.

        Examples:
            >>> import treebuilder as tb
            >>> builder = TreeBuilder()
            >>> builder.expand('bookstore/book/title', ['Sapiens', 'Harry Potter', 'A time of Mercy'])
            >>> builder.set('bookstore/book/is_in_stock', True)
            >>> print(builder.root)
            >>> builder.set('bookstore/book[title='Harry Potter']/price', 9.99)

        Returns:
            TreeBuilder: Returns the builder itself.
        """
        return self.expand(xpath, [value])

    def expand(self, xpath: str, values: List[Any]) -> 'TreeBuilder':
        """Expand the sub set tree with values

        This fuction use the `treebuilder.expand`. The source list is the tree sub 
        set selected by the given xpath and the last xpath tag is the entry key.
        For more details see the `treebuilder.expand` function documentation.

        Args:
            xpath: (str): The xpath to extract tree sub set
            value: (List[Any]): Values to apply for each leaf found.

        Examples:
            >>> import treebuilder as tb
            >>> builder = TreeBuilder()
            >>> builder.expand('bookstore/book/title', ['Sapiens', 'Harry Potter', 'A time of Mercy'])
            >>> builder.expand('bookstore/book/id', [1, 2, 3, 4, 5, 6])
            >>> builder.expand('bookstore/book[title='Harry Potter']/price', [9.99])
            >>> print(builder.root)

        Returns:
            TreeBuilder: Returns the builder itself.
        """
        entry, items = self.__get_items(xpath)
        items = expand(items, entry, values)
        self.__attach_items_to_tree(items, entry)
        return self

    def nest(self, xpath: str, values: List[Any]) -> 'TreeBuilder':
        """Nest the sub set tree with values.

        This fuction use the `treebuilder.nest`. The source list is the tree sub 
        set selected by the given xpath and the last xpath tag is the entry key.
        For more details see the `treebuilder.nest` function documentation.

        Args:
            xpath: (str): The xpath to extract tree sub set
            value: (List[Any]): Values to apply for each leaf found.

        Examples:
            >>> import treebuilder as tb
            >>> builder = TreeBuilder()
            >>> builder.expand('bookstore/book/title', ['Sapiens', 'Harry Potter', 'A time of Mercy'])
            >>> builder.nest('bookstore/book/id', [1, 2, 3, 4, 5, 6])
            >>> builder.nest('bookstore/book[title='Harry Potter']/price', [9.99])
            >>> print(builder.root)

        Returns:
            TreeBuilder: Returns the builder itself.
        """
        entry, items = self.__get_items(xpath)
        items = nest(items, entry, values)
        self.__attach_items_to_tree(items, entry)
        return self

    def cross(self, xpath: str, values: List[Any]) -> 'TreeBuilder':
        """Cross the sub set tree with values.

        This fuction use the `treebuilder.cross`. The source list is the tree sub 
        set selected by the given xpath and the last xpath tag is the entry key.
        For more details see the `treebuilder.cross` function documentation.

        Args:
            xpath: (str): The xpath to extract tree sub set
            value: (List[Any]): Values to apply for each leaf found.

        Examples:
            >>> import treebuilder as tb
            >>> builder = TreeBuilder()
            >>> builder.expand('bookstore/book/title', ['Sapiens', 'Harry Potter', 'A time of Mercy'])
            >>> builder.cross('bookstore/book/copy_number', [1, 2])
            >>> print(builder.root)

        Returns:
            TreeBuilder: Returns the builder itself.
        """
        entry, items = self.__get_items(xpath)
        items = cross(items, entry, values)
        self.__attach_items_to_tree(items, entry)
        return self

    def to_xml(self, file_path: str, root: str = None, pretty: bool = True):
        """Serialize the built tree to a XML file.

        Args:
            file_path (str): Xml file path
            root (str, optional): Additional xml root if needed. Defaults to None.
            pretty (bool, optional): Define if you want a human reading output or not. Defaults to True.
        """
        to_xml(self.__root, file_path, root=root, pretty=pretty)

    def to_json(self, file_path: str, pretty: bool = True):
        """Serialize the built tree to a JSON file.

        Args:
            file_path (str): JSON file path
            pretty (bool, optional): Define if you want a human reading output or not. Defaults to True.
        """
        to_json(self.__root, file_path, pretty=pretty)
    
    def __get_tag_and_filter(self, step: str) -> Tuple[str, str]:
        split = step.split('[')
        tag, filter = split[0], None

        if len(split) > 1 and split[-1].endswith(']'):
            split[-1] = split[-1][0:-1]
            filter = '['.join(split[1:len(split)])
        
        return tag, filter

    def __filter_items(self, items, syntax: str):
        self.__parser.items = items
        tokens = self.__lexer.tokenize(syntax)
        return self.__parser.parse(tokens)

    def __get_items(self, xpath: str) -> Tuple[str, List[Dict[str, Any]]]: 
        split = xpath.split('/')

        result = []
        queue = deque()
        queue.appendleft((0, self.__root, None))
        while len(queue) > 0:
            index, node, parent = queue.pop()

            step = split[index]
            if step == '':
                queue.appendleft((index + 1, node, parent))
                continue

            tag, filter = self.__get_tag_and_filter(step)

            is_leaf = index == len(split) - 1
            if is_leaf:
                node[PARENT] = parent
                result.append(node)
            else:
                # Create the node if it doesn't exist
                if tag not in node:
                    items = node[tag] = [{}]
                else:
                    # Get items for tag
                    items = node[tag]

                    # Filter items if asked
                    if filter is not None:
                        fil = self.__filter_items(items, filter)
                        items = [x for x in compress(items, fil)]
                        if len(items) == 0: # Make sure to hit leaf level
                            items = [{}]

                # Recursive walk
                for child in items:
                    queue.appendleft((index + 1, child, node[tag]))
        
        return split[-1], result

    def __attach_items_to_tree(self, items: List[Dict[str, Any]], entry: str):
        is_attribute = entry.startswith('@')
        att_entry = entry[1:len(entry)] if is_attribute else None
        
        # Todo: Improve complexity here by keeping a reference of the current parent and
        # playing with indices instead. This is possible because the order is kept by 
        # expand and cross functions.
        # This trick will avoid to iterate for each item on the full parent list and
        # improve the complexity from O(N x M) to O(N + M) where N is the number of 
        # created/updated items and M the number for items in the parent list which grows
        # in this loop
        for item in items:
            if item not in item[PARENT]:
                item[PARENT].append(item)
            item.pop(PARENT)

            if is_attribute:
                if ATTRIBUTES not in item:
                    item[ATTRIBUTES] = {}
                item[ATTRIBUTES][att_entry] = item[entry]
                item.pop(entry)
            
