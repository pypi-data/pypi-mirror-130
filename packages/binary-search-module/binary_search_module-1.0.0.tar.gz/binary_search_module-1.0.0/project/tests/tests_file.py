"""Done test by pytest"""
import pytest
from ..binary_search import bin_search


def main(number_list, number):
    return bin_search(number_list, number)


@pytest.mark.parametrize("number_list, number, result",  [([1, 2, 3, 3, 4, 81], 2, 1),
                                                          ([0, 1, 1, 2], 1, 1),
                                                          ([], 8, None),
                                                          ([1, 4, 4, 4, 5, 27, 81, 100], 4, 3),
                                                          ([1, 2, 5, 6, 7, 7, 7], 7, 5)])
def test_all_done(number_list, number, result):
    assert main(number_list, number) == result
