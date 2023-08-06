"""
Return required list of integer numbers
"""


from random import randint


def making_list_to_search():
	amount_numbers = input('Input how many number required: ')
	while not amount_numbers.isnumeric():
		amount_numbers = input('Incorrect input, try again: ')
	max_number = input('Input the biggest number: ')
	while not max_number.isnumeric() or max_number == '0':
		max_number = input('Incorrect input, try again: ')
	list_of_numbers = sorted(randint(-int(max_number), int(max_number)) for number in range(int(amount_numbers)))
	if not list_of_numbers:
		return None
	else:
		return list_of_numbers
