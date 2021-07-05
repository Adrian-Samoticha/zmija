import os
from glob import glob
import sys

from CommandLineArgHandler import CommandLineArgHandler
from FileManager import FileManager
from FileParser import FileParser
from FunctionHandler import FunctionHandler
from HelpPrinter import HelpPrinter

def main():
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
	file_paths = FileManager.get_file_paths(path)
	
	print("Found %d files."%len(file_paths))
	
	# Perform initialization pass.
	# This will execute the declare() and init() functions.
	print("Performing initialization pass...", end="")
	for file_path in file_paths:
		some_file = FileManager.open_file_readonly(file_path)
		FileParser.parse_file_initialization_pass(some_file)
		
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

if __name__ == '__main__':
	main()
