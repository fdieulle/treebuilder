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

    def set(self, xpath: str, value: Any, deep_copy: bool = True) -> 'TreeBuilder':
        """Set value for a tree sub set

        Args:
            xpath: (str): The xpath to extract tree sub set
            value: (Any): The value to apply for each leaf found.
            deep_copy (bool): Make a deep copy on values for each usages. Default is True.

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
        return self.expand(xpath, [value], deep_copy)

    def expand(self, xpath: str, values: List[Any], deep_copy: bool = True, from_ancestor: str = None) -> 'TreeBuilder':
        """Expand the sub set tree with values

        This fuction use the `treebuilder.expand`. The source list is the tree sub 
        set selected by the given xpath and the last xpath tag is the entry key.
        For more details see the `treebuilder.expand` function documentation.

        Args:
            xpath: (str): The xpath to extract tree sub set
            value: (List[Any]): Values to apply for each leaf found.
            deep_copy (bool): Make a deep copy on values for each usages. Default is True.
            from_ancestor (str): Select from which ancestor node you want to expand

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
        entry, items, parents = self.__get_items(xpath, from_ancestor)

        if from_ancestor is not None:
            # Generate ancestor nodes noly if needed
            if len(values) > len(items):
                nodes = self.__generate_ancestor_nodes_as_values(items, entry, len(values))
                items = expand(items, entry, nodes, deep_copy)
                self.__attach_items_to_tree(items, entry, parents)

            # Apply values (no more expansions)
            return self.expand(xpath, values, deep_copy)

        items = expand(items, entry, values, deep_copy)
        self.__attach_items_to_tree(items, entry, parents)

        return self

    def nest(self, xpath: str, values: List[Any], deep_copy: bool = True) -> 'TreeBuilder':
        """Nest the sub set tree with values.

        This fuction use the `treebuilder.nest`. The source list is the tree sub 
        set selected by the given xpath and the last xpath tag is the entry key.
        For more details see the `treebuilder.nest` function documentation.

        Args:
            xpath: (str): The xpath to extract tree sub set
            value: (List[Any]): Values to apply for each leaf found.
            deep_copy (bool): Make a deep copy on values for each usages. Default is True.

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
        entry, items, parents = self.__get_items(xpath)
        items = nest(items, entry, values, deep_copy)
        self.__attach_items_to_tree(items, entry, parents)

        return self

    def cross(self, xpath: str, values: List[Any], deep_copy: bool = True, from_ancestor: str = None) -> 'TreeBuilder':
        """Cross the sub set tree with values.

        This fuction use the `treebuilder.cross`. The source list is the tree sub 
        set selected by the given xpath and the last xpath tag is the entry key.
        For more details see the `treebuilder.cross` function documentation.

        Args:
            xpath: (str): The xpath to extract tree sub set
            value: (List[Any]): Values to apply for each leaf found.
            deep_copy (bool): Make a deep copy on values for each usages. Default is True.
            from_ancestor (str): Select from which ancestor node you want to expand

        Examples:
            >>> import treebuilder as tb
            >>> builder = TreeBuilder()
            >>> builder.expand('bookstore/book/title', ['Sapiens', 'Harry Potter', 'A time of Mercy'])
            >>> builder.cross('bookstore/book/copy_number', [1, 2])
            >>> print(builder.root)

        Returns:
            TreeBuilder: Returns the builder itself.
        """            
        entry, items, parents = self.__get_items(xpath, from_ancestor)

        if from_ancestor is not None and len(values) != 0:
            # Generate ancestors
            nodes = self.__generate_ancestor_nodes_as_values(items, entry, len(items) * len(values))
            items = expand(items, entry, nodes, deep_copy)
            self.__attach_items_to_tree(items, entry, parents)

            # Generate crossed values
            repeats = int(len(items) / len(values))
            crossed_values = []
            for value in values:
                crossed_values += [value for x in range(repeats)]
            
            # Apply values (no more expansions)
            self.expand(xpath, crossed_values, deep_copy)
        else:
            items = cross(items, entry, values, deep_copy)
            self.__attach_items_to_tree(items, entry, parents)

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
    
    def get_items(self, xpath: str, unlist: bool = True) -> List[Any]:
        """Get sub set tree elements

        Args:
            xpath (str): The xpath to extract tree sub set
            unlist (bool): Unlist nodes if they are request. If you request leaves which 
                are type of list you should set this parameter to False. True by default.

        Returns:
            List[Any]: Returns the sub set tree elements find by the xpath.
        """
        # Todo: see how to share more code with __attach_items_to_tree
        entry, items, parents = self.__get_items(xpath)
        
        # Remove internal stuff
        [item.pop(PARENT) for item in items]

        if entry.startswith('@'): # It's an attribute
            entry = entry[1:len(entry)]
            return [x[ATTRIBUTES][entry] if ATTRIBUTES in x and entry in x[ATTRIBUTES] else None for x in items]

        items = [x[entry] if entry in x else None for x in items]
        if not unlist:
            return items

        result = []
        for item in items:
            if type(item) is list:
                [result.append(x) for x in item]
            else:
                result.append(item)
        return result

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

    def __get_items(self, xpath: str, from_ancestor: str = None) -> Tuple[str, List[Dict[str, Any]], Dict[str, List]]: 
        split = xpath.split('/')
        max_depth = len(split) - 1

        result, parents = [], {}
        queue = deque()
        queue.appendleft((0, self.__root, None))
        while len(queue) > 0:
            index, node, parent = queue.pop()

            step = split[index]
            if step == '':
                queue.appendleft((index + 1, node, parent))
                continue

            tag, filter = self.__get_tag_and_filter(step)

            if tag == from_ancestor:
                max_depth = index + 1

            is_leaf = index == max_depth
            if is_leaf:
                parent_id = len(parents)
                node[PARENT] = parent_id
                parents[parent_id] = parent
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
        
        return split[max_depth], result, parents

    def __generate_ancestor_nodes_as_values(self, items, entry, target_length):
        i, values = 0, []

        while i < target_length:
            for item in items:
                values.append(item[entry] if entry in item else [{}])
                
                i += 1
                if i >= target_length:
                    break
        
        return values
        
        
    def __attach_items_to_tree(self, items: List[Dict[str, Any]], entry: str, parents: Dict[str, List]):
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
            parent = parents[item[PARENT]]
            if item not in parent:
                parent.append(item)
            item.pop(PARENT)

            if is_attribute:
                if ATTRIBUTES not in item:
                    item[ATTRIBUTES] = {}
                item[ATTRIBUTES][att_entry] = item[entry]
                item.pop(entry)
            
