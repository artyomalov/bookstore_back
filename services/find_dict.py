"""
Find dict in array
"""

__all__ = ['find_dict_in_list', ]


def find_dict_in_list(array, compare_function) -> dict | None:
    """
    Iterate array and return dict if there is a dict relevant
    for find_by condition and false if not
    """

    for element in array:
        flag = compare_function(element)
        print(flag)
        if flag is True:
            return element
    return None
    # in_list_flag = True
    # for dictionary in array:
    #     for i in range(len(find_by)):
    #         print(dictionary[find_by[i]])
    #         if dictionary[find_by[i]] != find_value[i]:
    #             nonlocal in_list_flag
    #             in_list_flag = False
    #     if in_list_flag is True:
    #         return dict

    #
    # if dictionary.get(find_by[0]) == find_value[0] and dictionary.get(
    #         find_by[1]) == find_value[1]:
    #     return dictionary
    return None
