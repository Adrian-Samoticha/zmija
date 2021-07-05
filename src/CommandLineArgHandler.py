import sys

class CommandLineArgHandler:
	def get_path():
		if len(sys.argv) < 2:
			return "."
		return sys.argv[1]
		
	def get_is_requesting_help():
		return "-h" in sys.argv