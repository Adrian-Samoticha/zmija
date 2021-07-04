class StringUtility:
	def get_indentation_of_line(some_string):
		count = 0
		while count < len(some_string) and some_string[count] in ['\t', ' ']:
			count += 1
		return count
		
	def reduce_indentation_of_line(some_string, amount):
		return some_string[amount:]
		
	def indent_multiline_string(some_string, amount):
		some_string = "\n" + some_string
		some_string = some_string.replace("\n", "\n" + "\t" * amount)
		return some_string[1:]