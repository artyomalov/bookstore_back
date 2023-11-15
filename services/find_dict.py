"""
Find dict in array
"""

__all__ = ['find_dict_in_list', ]


def find_dict_in_list(find_by='id', find_value=1, array=None) -> dict | None:
    """
    Iterate array and return dict if there is a dict relevant
    for find_by condition and false if not
    """
    if array is None:
        return None
    for dictionary in array:
        if dictionary.get(find_by) == find_value:
            return dictionary
    return None
