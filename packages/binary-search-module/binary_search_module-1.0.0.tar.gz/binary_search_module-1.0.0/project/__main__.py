"""
Main package's module

Borisyuk Kirill
hurricanekba@gmail.com

bin_search - done binary search in list
making_list_to_search - return required list
enter_numbers - return required number
"""


import argparse
import doctest
import pytest
from binary_search import bin_search
from make_list_to_search import making_list_to_search
from number_giver import enter_numbers


CLI = argparse.ArgumentParser(description='searching number by binary method in given list')
CLI.add_argument('regime_selection', type=str, default='binary', help='Regimes:'
                                                                      '"binary" - start main func'
                                                                      '"test" - start tests with pytest'
                                                                      '"doctest" - start tests with pytest')
args = CLI.parse_args()


def main():
    """Return main function"""
    if args.regime_selection == 'binary':
        result = bin_search((list_to_print := making_list_to_search()), enter_numbers())
        if result is None:
            print('There is no such number in the list or list is empty')
        else:
            return print(fr'Required number has index [{result}] in {list_to_print}')
    elif args.regime_selection == 'test':
        """Return logs about pytests"""
        return pytest.main([r"C:\Users\hurri\Project2\project\tests\tests_file.py"])
    elif args.regime_selection == 'doctest':
        """Return logs about dostest"""
        return doctest.testfile(r"C:\Users\hurri\Project2\project\doctesttry.txt", verbose='-v')


if __name__ == '__main__':
    main()
