def enter_numbers():
	"""Entering the required number with checking"""
	correct_number_flag = 0
	while correct_number_flag != 1:
		number = input('Input required number: ')
		try:
			number = int(number)
			correct_number_flag = 1
			return number
		except ValueError:
			print('Incorrect input. Try again')
