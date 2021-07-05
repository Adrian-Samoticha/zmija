import sys

class CommandLineArgHandler:
	def get_path():
		if len(sys.argv) < 2:
			return "."
		return sys.argv[1]