def print_lol(the_list):
	
	for each_item in the_list:
		if isinstance(each_item, list):
			print_lol_re(each_item)
		else:
			print(each_item)
