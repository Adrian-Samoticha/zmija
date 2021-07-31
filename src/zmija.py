import os
from glob import glob
import sys

from CommandLineArgHandler import CommandLineArgHandler
from FileManager import FileManager
from FileParser import FileParser
from FunctionHandler import FunctionHandler
from HelpPrinter import HelpPrinter

class Zmija:
	def get_command_line_arguments():
		CommandLineArgHandler.check_args()
		
		if (CommandLineArgHandler.get_is_requesting_help()):
			HelpPrinter.print_help()
			sys.exit()
		
		do_delete = CommandLineArgHandler.get_is_requesting_delete()
		do_perform_check_only = CommandLineArgHandler.get_is_requesting_check_only()
		do_skip_test_pass = CommandLineArgHandler.get_is_requesting_unsafe()
		
		if do_perform_check_only and do_skip_test_pass:
			print("Error: --unsafe is incompatible with --check-only")
			sys.exit(1)
		
		path = CommandLineArgHandler.get_path()
		
		config = {
			"file_filter": lambda x: True
		}
		config_path = CommandLineArgHandler.get_config_path()
		if config_path != None:
			if not os.path.isfile(config_path):
				print("Error: config file does not exist (file path: \"%s\")" % config_path)
				sys.exit(1)
			config_file = FileManager.open_file_readonly(config_path)
			config_file_text = config_file.read()
			exec(config_file_text + "\n_config_dictionary['file_filter'] = file_filter", {"_config_dictionary": config})
			config_file.close()
		
		return (do_delete, do_perform_check_only, do_skip_test_pass, path, config["file_filter"])
	
	def run(do_delete, do_perform_check_only, do_skip_test_pass, path, filter):
		file_paths = FileManager.get_file_paths(path)
		file_paths = [file_path for file_path in file_paths if filter(file_path)]
		
		print("Found %d files." % len(file_paths))
		
		# Perform initialization pass.
		# This will execute the declare() and init() functions.
		print("Performing initialization pass...", end="")
		for file_path in file_paths:
			some_file = FileManager.open_file_readonly(file_path)
			FileParser.parse_file_initialization_pass(some_file)
			some_file.close()
			
		FunctionHandler.execute_functions()
		print("done.")
		
		# Perform generation pass without actually writing to the files.
		# This will catch errors in the generator functions without
		# damaging the source code files.
		if (not do_skip_test_pass):
			print("Performing test generation pass...", end="")
			for file_path in file_paths:
				some_file = FileManager.open_file_readonly(file_path)
				new_content = FileParser.parse_file_generation_pass(some_file, do_delete)
				some_file.close()
			print("done.")
			
		if do_perform_check_only:
			return
		
		# Perform generation pass and write changes to the files.
		print("Performing actual generation pass...", end="")
		for file_path in file_paths:
			some_file = FileManager.open_file_readonly(file_path)
			new_content = FileParser.parse_file_generation_pass(some_file, do_delete)
			some_file.close()
			some_file = FileManager.open_file_writeonly(file_path)
			some_file.write(new_content)
			some_file.close()
		print("done.")
	
	def main():
		(do_delete, do_perform_check_only, do_skip_test_pass, path, filter) = Zmija.get_command_line_arguments()
		Zmija.run(do_delete, do_perform_check_only, do_skip_test_pass, path, filter)

if __name__ == '__main__':
	Zmija.main()
