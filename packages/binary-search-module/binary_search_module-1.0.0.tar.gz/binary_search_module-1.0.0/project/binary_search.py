def bin_search(created_list, desired_number):
	"""Done search in given list by binary method"""
	if created_list:
		lower_index = 0
		upper_index = len(created_list) - 1
		while lower_index <= upper_index:
			mid_index = (lower_index + upper_index)//2
			if created_list[mid_index] == desired_number:
				return mid_index
			elif created_list[mid_index] > desired_number:
				upper_index = mid_index - 1
			elif created_list[mid_index] < desired_number:
				lower_index = mid_index + 1
		return None
	else:
		return None
