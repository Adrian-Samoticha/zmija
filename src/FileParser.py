import enum
import traceback
import sys

from util.StringUtility import StringUtility
from FunctionHandler import FunctionHandler

class InitializationCodeParser:
	_initialization_code = ""
	_indent_level = 0
	
	def _complete_initialization_code(self, code):
		return """
def declare(variables):
	pass

def init(variables):
	pass
""" + \
		       code + \
		       "\nFunctionHandler.add_function(declare, init)"
	
	def _reset(self):
		self._initialization_code = ""
		self._indent_level = 0
		
	def add_line(self, line):
		# The Python code in the source file may be indented.
		# Since Python is sensitive to indentation, the input
		# needs to be sanitized accordingly.
		# An empty '_initialization_code' signalizes that we are
		# reading the first line. Therefore, we calculate the 
		# indentation level now.
		if self._initialization_code == "":
			self._indent_level = StringUtility.get_indentation_of_line(line)
		self._initialization_code += StringUtility.reduce_indentation_of_line(line, self._indent_level)
		
	def parse(self):
		completed_code = self._complete_initialization_code(self._initialization_code)
		try:
			exec(completed_code)
		except SyntaxError:
			print("SYNTAX ERROR:\n", traceback.format_exc())
			print("Exiting Zmija.")
			sys.exit()
		except (NameError, ValueError) as err:
			print("RUNTIME ERROR:\n", err)
			print("Exiting Zmija.")
			sys.exit()
			
		self._reset()
		
class GenerationCodeParser:
	_generation_code = ""
	_indent_level = 0
	
	def _complete_generation_code(self, code):
		return """
def generate(variables):
	return ""
""" + \
		       code + \
		       "\nFunctionHandler.generate_function_return_value = generate(FunctionHandler.variables)"
	
	def _reset(self):
		self._generation_code = ""
		self._indent_level = 0
		
	def add_line(self, line):
		# The Python code in the source file may be indented.
		# Since Python is sensitive to indentation, the input
		# needs to be sanitized accordingly.
		# An empty '_generation_code' signalizes that we are
		# reading the first line. Therefore, we calculate the 
		# indentation level now.
		if self._generation_code == "":
			self._indent_level = StringUtility.get_indentation_of_line(line)
		self._generation_code += StringUtility.reduce_indentation_of_line(line, self._indent_level)
		
	def parse(self):
		completed_code = self._complete_generation_code(self._generation_code)
		try:
			exec(completed_code)
		except SyntaxError:
			print("SYNTAX ERROR:\n", traceback.format_exc())
			print("Exiting Zmija.")
			sys.exit()
		except (NameError, ValueError) as err:
			print("RUNTIME ERROR:\n", err)
			print("Exiting Zmija.")
			sys.exit()
		return_value = FunctionHandler.generate_function_return_value
		return_value = StringUtility.indent_multiline_string(return_value, self._indent_level) + "\n"
		self._reset()
		return return_value
		
class ParseState(enum.Enum):
	SEARCHING = 0
	FOUND_GENERATOR = 1
	FOUND_GENERATED_CODE = 2

class FileParser:	
	def parse_file_initialization_pass(some_file):
		parse_state = ParseState.SEARCHING
		initialization_code_parser = InitializationCodeParser()
		for line in some_file:
			stripped_line = line.strip()
			if parse_state == ParseState.SEARCHING:
				if stripped_line.endswith("~ZMIJA.GENERATOR:"):
					parse_state = ParseState.FOUND_GENERATOR
				
			elif parse_state == ParseState.FOUND_GENERATOR:
				if stripped_line.endswith("~ZMIJA.GENERATED_CODE:"):
					initialization_code_parser.parse()
					parse_state = ParseState.FOUND_GENERATED_CODE
				else:
					initialization_code_parser.add_line(line)
			elif parse_state == ParseState.FOUND_GENERATED_CODE:
				if stripped_line.endswith("~ZMIJA.END"):
					parse_state = ParseState.SEARCHING
					
	def parse_file_generation_pass(some_file, do_delete):
		new_content = ""
		
		parse_state = ParseState.SEARCHING
		generation_code_parser = GenerationCodeParser()
		for line in some_file:
			stripped_line = line.strip()
			if parse_state == ParseState.SEARCHING:
				if stripped_line.endswith("~ZMIJA.GENERATOR:"):
					parse_state = ParseState.FOUND_GENERATOR
					
				new_content += line
			
			elif parse_state == ParseState.FOUND_GENERATOR:
				new_content += line
				
				if stripped_line.endswith("~ZMIJA.GENERATED_CODE:"):
					new_content += generation_code_parser.parse() if not do_delete else "\n"
					parse_state = ParseState.FOUND_GENERATED_CODE
				else:
					generation_code_parser.add_line(line)
			elif parse_state == ParseState.FOUND_GENERATED_CODE:
				if stripped_line.endswith("~ZMIJA.END"):
					new_content += line
					parse_state = ParseState.SEARCHING
		
		return new_content