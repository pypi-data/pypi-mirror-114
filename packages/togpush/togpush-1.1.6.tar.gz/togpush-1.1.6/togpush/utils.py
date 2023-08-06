from typing import Any, List


def chunk_list(list_: List[Any], chunks: int = 20) -> List[List[Any]]:
    """
    Group elements in a list together.

    ```ipython
    In [13]: list(range(22))
    Out[13]: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
    ```

    ```ipython
    In [12]: list(chunk_list(list(range(22)), 3))
    Out[12]:
    [[0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [9, 10, 11],
    [12, 13, 14],
    [15, 16, 17],
    [18, 19, 20],
    [21]]
    ```

    :param list_: An arbitrary list.
    :type list_: List[Any]
    :param chunks: Size of a group of elements from the main list to make sub-lists.
    :type chunks: int
    """
    for i in range(0, len(list_), chunks):
        yield list_[i:i+chunks]
