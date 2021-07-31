import sys

class CommandLineArgHandler:
	_known_args = [
		("help", 'h'),
		("delete", 'd'),
		("check-only", 'c'),
		("unsafe", 'u'),
		("config-path", None)
	]
	
	
	def _check_option_exists(long, short):
		if "--" + long in map(lambda x: x.split('=')[0], sys.argv):
			return True
			
		if short == None:
			return False
			
		for arg in sys.argv:
			if arg.startswith('-') and not arg.startswith("--") and short in arg:
				return True
		return False
		
	def _get_value(long):
		for arg in sys.argv:
			splits = arg.split('=')
			if splits[0] == "--" + long and len(splits) >= 2:
				return splits[1]
			
		return None
		
	def check_args():
		for i in range(2, len(sys.argv)):
			if sys.argv[i].startswith("--"):
				arg_name = sys.argv[i].split('=')[0]
				if arg_name not in map(lambda x: "--" + x[0], CommandLineArgHandler._known_args):
					print("Unknown argument: %s" % arg_name)
					sys.exit(1)
			elif sys.argv[i].startswith("-"):
				for c in sys.argv[i]:
					if c != '-' and c not in map(lambda x: x[1], CommandLineArgHandler._known_args):
						print("Unknown argument: %s" % c)
						sys.exit(1)
	
	def get_path():
		if len(sys.argv) < 2:
			return "."
		return sys.argv[1].strip('"')
		
	def get_is_requesting_help():
		return CommandLineArgHandler._check_option_exists("help", 'h')
		
	def get_is_requesting_delete():
		return CommandLineArgHandler._check_option_exists("delete", 'd')
		
	def get_is_requesting_check_only():
		return CommandLineArgHandler._check_option_exists("check-only", 'c')
		
	def get_is_requesting_unsafe():
		return CommandLineArgHandler._check_option_exists("unsafe", 'u')
		
	def get_config_path():
		result = CommandLineArgHandler._get_value("config-path")
		if result == None:
			return None
		return result.strip('"')