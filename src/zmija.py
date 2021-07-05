import os
from glob import glob

from FileManager import FileManager
from FileParser import FileParser
from FunctionHandler import FunctionHandler

def main():
	path = "../test_project/"
	file_paths = FileManager.get_file_paths(path)
	
	# Perform initialization pass.
	# This will execute the declare() and init() functions.
	for file_path in file_paths:
		some_file = FileManager.open_file_readonly(file_path)
		FileParser.parse_file_initialization_pass(some_file)
		
	FunctionHandler.execute_functions()
	
	# Perform generation pass without actually writing to the files.
	# This will catch errors in the generator functions without
	# damaging the source code files.
	for file_path in file_paths:
		some_file = FileManager.open_file_readonly(file_path)
		new_content = FileParser.parse_file_generation_pass(some_file)
	
	# Perform generation pass and write changes to the files.
	for file_path in file_paths:
		some_file = FileManager.open_file_readonly(file_path)
		new_content = FileParser.parse_file_generation_pass(some_file)
		some_file_writeonly = FileManager.open_file_writeonly(file_path)
		some_file_writeonly.write(new_content)

if __name__ == '__main__':
	main()
