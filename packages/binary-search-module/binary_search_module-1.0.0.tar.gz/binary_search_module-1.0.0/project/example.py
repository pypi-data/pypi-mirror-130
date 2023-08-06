"""
Module for example.

Searching value in list by binary search metod, examples down below.

>>> main([1, 2, 4, 5, 6, 8, 8], 2)
1

>>> main([1, 6, 6, 7, 2, 2, 2, 0, 9], 2)
4

>>> main([], 2)
List is empty
"""


def main(number_list, number):
    from binary_search import bin_search
    return bin_search(number_list, number)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
