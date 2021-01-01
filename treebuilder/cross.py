from typing import Any, Dict, List


# Todo: maybe it should be better to returns an iterable instead of a list
def cross(source: List[Dict[str, Any]], entry: str, values: List[Any]) -> List[Dict[str, Any]]:
    if len(source) == 0: # Todo: Maybe not because 0 x N should be = 0 as it does for N x 0 here
        return [{ entry: v } for v in values]
    
    result = []
    if len(values) > 0:
        # First we modify the existing objects
        for item in source:
            item[entry] = values[0]
            result.append(item)

    for value in values[1:len(values)]:
        for item in source:
            copy = item.copy() # Todo: Proably need a deep copy here
            copy[entry] = value
            result.append(copy)

    return result
    
        
