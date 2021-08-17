class StringUtility:
	def get_indentation_of_line(some_string):
		count = 0
		while count < len(some_string) and some_string[count] in ['\t', ' ']:
			count += 1
		return count
		
	def reduce_indentation_of_line(some_string, amount):
		return some_string[amount:]
		
	def indent_multiline_string(some_string, amount, indent_character):
		some_string = "\n" + some_string
		some_string = some_string.replace("\n", "\n" + indent_character * amount)
		return some_string[1:]
		
	def _get_comment_start_length(lines):
		length = 0
		while True:
			if length >= len(lines[0]):
				return length
			char_to_check_for = lines[0][length]
			for i in range(1, len(lines)):
				if length >= len(lines[i]):
					return length
				if lines[i][length] != char_to_check_for:
					return length
			length += 1
		
	def _remove_comments_from_lines(lines, comment_start_length):
		remove_comment_start = lambda x: x[comment_start_length:]
		return list(map(remove_comment_start, lines))

	def uncomment_code(some_code):
		lines = [i for i in some_code.split("\n") if i != '']
		comment_start_length = StringUtility._get_comment_start_length(lines)
		commented_out_lines = StringUtility._remove_comments_from_lines(lines, comment_start_length)
		return "\n".join(commented_out_lines)