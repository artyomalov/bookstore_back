"""
Find dict in array
"""

__all__ = ['find_dict_in_list', ]


def find_dict_in_list(find_by, find_value, array) -> dict | None:
    """
    Iterate array and return dict if there is a dict relevant
    for find_by condition and false if not
    """
    for dictionary in array:
        if dictionary.get(find_by[0]) == find_value[0] and dictionary.get(
                find_by[1]) == find_value[1]:
            return dictionary
    return None
