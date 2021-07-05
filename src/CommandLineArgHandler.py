import sys

class CommandLineArgHandler:
	_known_args = [
		("help", 'h'),
		("delete", 'd'),
		("check-only", 'c'),
		("unsafe", 'u')
	]
	
	
	def _get_does_option_exist(long, short):
		if "--" + long in sys.argv:
			return True
			
		for arg in sys.argv:
			if arg.startswith('-') and not arg.startswith("--") and short in arg:
				return True
		return False
		
	def check_args():
		for i in range(2, len(sys.argv)):
			if sys.argv[i].startswith("--"):
				if sys.argv[i] not in map(lambda x: "--" + x[0], CommandLineArgHandler._known_args):
					print("Unknown argument: %s" % sys.argv[i])
					sys.exit(1)
			elif sys.argv[i].startswith("-"):
				for c in sys.argv[i]:
					if c != '-' and c not in map(lambda x: x[1], CommandLineArgHandler._known_args):
						print("Unknown argument: %s" % c)
						sys.exit(1)
	
	def get_path():
		if len(sys.argv) < 2:
			return "."
		return sys.argv[1]
		
	def get_is_requesting_help():
		return CommandLineArgHandler._get_does_option_exist("help", 'h')
		
	def get_is_requesting_delete():
		return CommandLineArgHandler._get_does_option_exist("delete", 'd')
		
	def get_is_requesting_check_only():
		return CommandLineArgHandler._get_does_option_exist("check-only", 'c')
		
	def get_is_requesting_unsafe():
		return CommandLineArgHandler._get_does_option_exist("unsafe", 'u')