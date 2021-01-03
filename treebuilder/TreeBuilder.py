from typing import Any, Dict, List, Tuple
from collections import deque
from itertools import compress

from treebuilder.constants import ATTRIBUTES, PARENT
from treebuilder.FilterLexer import FilterLexer
from treebuilder.FilterParser import FilterParser
from treebuilder.expand import expand
from treebuilder.cross import cross
from treebuilder.xml import to_xml
from treebuilder.json import to_json


class TreeBuilder:

    def __init__(self):
        self.root = {}
        self.__lexer = FilterLexer()
        self.__parser = FilterParser()

    def set(self, xpath: str, value) -> 'TreeBuilder':
        return self.expand(xpath, [value])

    def expand(self, xpath: str, values: List[Any]) -> 'TreeBuilder':
        entry, items = self.__get_items(xpath)
        items = expand(items, entry, values)
        self.__attach_items_to_tree(items, entry)
        return self

    def cross(self, xpath: str, values: List[Any]) -> 'TreeBuilder':
        entry, items = self.__get_items(xpath)
        items = cross(items, entry, values)
        self.__attach_items_to_tree(items, entry)
        return self

    def to_xml(self, file_path: str, root: str = None, pretty: bool = True):
        to_xml(self.root, file_path, root=root, pretty=pretty)

    def to_json(self, file_path: str, root: str = None, pretty: bool = True):
        to_json(self.root, file_path, pretty=pretty)
    
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
        queue.appendleft((0, self.root, None))
        while len(queue) > 0:
            index, node, parent = queue.pop()

            step = split[index]
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
        
        if is_attribute:
            att_entry = entry[1:len(entry)] # Remove the @
            for item in items:
                
                if ATTRIBUTES not in item:
                    item[ATTRIBUTES] = {}

                item[ATTRIBUTES][att_entry] = item[entry]
                item.pop(entry)
                item.pop(PARENT)
        else:
            for item in items:
                if item not in item[PARENT]:
                    item[PARENT].append(item)
                item.pop(PARENT)
