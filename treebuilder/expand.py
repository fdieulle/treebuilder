from typing import Any, Dict, List


# Todo: maybe it should be better to returns an iterable instead of a list
def expand(source: List[Dict[str, Any]], entry: str, values: List[Any]) -> List[Dict[str, Any]]:
    """Expand source by a values list 

    When both source and values have the same length, the expansion is applied only
    on each source item by setting values to the entry key one by one.
    If their length are different, the expansion can alsoe applies on either the source and 
    values lists length.

    The shorter list rolls until reaching the end of the longer by using a ring logic.
    A list used as a ring means that when the end of this list is reached we go back to 
    the first element then continue iteration.

    Exemples:
        >>> import treebuilder as tb
        >>> x = []
        >>> y = tb.expand(x, 'Name', ['Sapiens', 'Harry Potter', 'A Time of Mercy'])
        >>> print(y)
        >>> z = tb.expand(y, 'Id', [1, 2, 3])
        >>> print(z)

        >>> x = [{'Name': 'foo'}, {'Name': 'bar'}]
        >>> y = tb.expand(x, 'Value', [1])
        >>> print(y)
        >>> y = tb.expand(x, 'Value', [1, 2, 3])
        >>> print(y)

    Args:
        source (List[Dict[str, Any]]): Source list to expand.
        entry (str): Entry key under which values are stored.
        values (List[Any]): List of values to expand.

    Returns:
        List[Dict[str, Any]]: The expanded list.
    """
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
