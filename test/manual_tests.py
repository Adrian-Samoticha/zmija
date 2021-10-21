import unittest
import os
from os.path import exists
import shutil
import sys

testdir = os.path.dirname(__file__)
srcdir = '../src'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

from zmija import Zmija

class ManualTest(unittest.TestCase):
	def _remove_directory(self, path):
		try:
			shutil.rmtree(path)
		except OSError as e:
			print("Directory deletion failed: %s - %s." % (e.filename, e.strerror))
	
	def test_manually_1(self):
		PATH = "./test/test_project/"
		if exists(PATH):
			self._remove_directory(PATH)
		os.mkdir(PATH)
		file1 = open(PATH + "file1.txt", 'x')
		file1.write("""begin
/* ~ZMIJA.GENERATOR:
def declare(variables):
	variables["file1_list"] = []
	pass
	
def init(variables):
	variables["file2_list"].append("TEXT_FILE1")
	pass
	
def generate(variables):
	return "\\n".join(variables["file1_list"])
*/// ~ZMIJA.GENERATED_CODE:

// ~ZMIJA.END
end
""")
		file1.close()
		file2 = open(PATH + "file2.txt", 'x')
		file2.write("""begin
/* ~ZMIJA.GENERATOR:
def declare(variables):
	variables["file2_list"] = []
	pass
	
def init(variables):
	variables["file1_list"].append("TEXT_FILE2")
	pass
	
def generate(variables):
	return "\\n".join(variables["file2_list"])
*/// ~ZMIJA.GENERATED_CODE:

// ~ZMIJA.END
end
""")
		file2.close()
		Zmija.run(False, False, False, PATH, lambda x: True)
		
		file1 = open(PATH + "file1.txt", "r")
		self.assertEqual(file1.read(), """begin
/* ~ZMIJA.GENERATOR:
def declare(variables):
	variables["file1_list"] = []
	pass
	
def init(variables):
	variables["file2_list"].append("TEXT_FILE1")
	pass
	
def generate(variables):
	return "\\n".join(variables["file1_list"])
*/// ~ZMIJA.GENERATED_CODE:
TEXT_FILE2
// ~ZMIJA.END
end
""")
		file1.close()
		file2 = open(PATH + "file2.txt", "r")
		self.assertEqual(file2.read(), """begin
/* ~ZMIJA.GENERATOR:
def declare(variables):
	variables["file2_list"] = []
	pass
	
def init(variables):
	variables["file1_list"].append("TEXT_FILE2")
	pass
	
def generate(variables):
	return "\\n".join(variables["file2_list"])
*/// ~ZMIJA.GENERATED_CODE:
TEXT_FILE1
// ~ZMIJA.END
end
""")
		file2.close()
		self._remove_directory(PATH)
		
	def test_manually_2(self):
		PATH = "./test/test_project/"
		if exists(PATH):
			self._remove_directory(PATH)
		os.mkdir(PATH)
		file = open(PATH + "file.txt", 'x')
		file.write("""begin
	some indentation:
		/* ~ZMIJA.GENERATOR:
		def declare(variables):
			variables["first_list"] = []
			pass
			
		def init(variables):
			variables["second_list"].append("ONE")
			variables["third_list"].append("ONE")
			pass
			
		def generate(variables):
			return "\\n".join(variables["first_list"])
		*/// ~ZMIJA.GENERATED_CODE:
		SOME GARBAGE
		// ~ZMIJA.END
upper middle
	even more:
		indentation:
			/* ~ZMIJA.GENERATOR:
			def declare(variables):
				variables["second_list"] = []
				pass
				
			def init(variables):
				variables["first_list"].append("TWO")
				variables["third_list"].append("TWO")
				pass
				
			def generate(variables):
				return "\\n".join(variables["second_list"])
			*/// ~ZMIJA.GENERATED_CODE:
			SOME GARBAGE
			// ~ZMIJA.END
lower middle
/* ~ZMIJA.GENERATOR:
def declare(variables):
	variables["third_list"] = []
	pass
	
def init(variables):
	variables["first_list"].append("THREE")
	variables["second_list"].append("THREE")
	pass
	
def generate(variables):
	return "\\n".join(variables["third_list"])
*/// ~ZMIJA.GENERATED_CODE:
SOME GARBAGE
// ~ZMIJA.END
end""")
		file.close()
		
		Zmija.run(False, False, False, PATH, lambda x: True)
		
		file = open(PATH + "file.txt", "r")
		self.assertEqual(file.read(), """begin
	some indentation:
		/* ~ZMIJA.GENERATOR:
		def declare(variables):
			variables["first_list"] = []
			pass
			
		def init(variables):
			variables["second_list"].append("ONE")
			variables["third_list"].append("ONE")
			pass
			
		def generate(variables):
			return "\\n".join(variables["first_list"])
		*/// ~ZMIJA.GENERATED_CODE:
		TWO
		THREE
		// ~ZMIJA.END
upper middle
	even more:
		indentation:
			/* ~ZMIJA.GENERATOR:
			def declare(variables):
				variables["second_list"] = []
				pass
				
			def init(variables):
				variables["first_list"].append("TWO")
				variables["third_list"].append("TWO")
				pass
				
			def generate(variables):
				return "\\n".join(variables["second_list"])
			*/// ~ZMIJA.GENERATED_CODE:
			ONE
			THREE
			// ~ZMIJA.END
lower middle
/* ~ZMIJA.GENERATOR:
def declare(variables):
	variables["third_list"] = []
	pass
	
def init(variables):
	variables["first_list"].append("THREE")
	variables["second_list"].append("THREE")
	pass
	
def generate(variables):
	return "\\n".join(variables["third_list"])
*/// ~ZMIJA.GENERATED_CODE:
ONE
TWO
// ~ZMIJA.END
end""")
		file.close()
		self._remove_directory(PATH)
		
	
if __name__ == '__main__':
	unittest.main()