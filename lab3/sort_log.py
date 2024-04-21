from operator import itemgetter
from typing import List, Tuple


def sort_log(tuple_list: List[Tuple], order_element: int):
    try:
        result = sorted(tuple_list, key=itemgetter(order_element))
    except IndexError:
        print("Choose number between 0 and 5!")
    return result
