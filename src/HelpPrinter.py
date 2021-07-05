class HelpPrinter:
	def print_help():
		print("""Zmija. Simple universal code generation.

Usage:
	zmija.py path
	zmija.py path -d | --delete
	zmija.py path -c | --check-only
	zmija.py -h | --help
	
Options:
	-h --help         Show this screen.
	-d --delete       Delete all generated code.
	-c --check-only   Check Python code for syntax and runtime errors without writing the changes to file.
	-u --unsafe       Skip the test pass. May cause data loss if the Python code raises exceptions, but offers better performance. Use with caution.""")