import itertools
from typing import Any, Dict, List


def expand(source: List[Dict[str, Any]], entry: str, values: List[Any]) -> List[Dict[str, Any]]:
    if len(values) == 0:
        return source

    result = []
    # Add values as a ring to the sources
    index = 0
    should_expand_source = True
    for item in source:
        if index == len(values):
            index = 0
            should_expand_source = False
        
        item[entry] = values[index]
        index += 1
        result.append(item)

    # If the values is longer than the source
    if should_expand_source:
        if len(source) > 0:
            # We ring around the source valuse to duplicate then set the value
            while index < len(values):
                for item in source:
                    if index == len(values):
                        break
                    copy = item.copy() # Todo: Proably need a deep copy here
                    copy[entry] = values[index]
                    index += 1
                    result.append(copy)
        else:
            # The source is empty so we build full new values
            while index < len(values):
                result.append({ entry: values[index] })
                index += 1
    
    return result
