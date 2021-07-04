import os
from glob import glob

class FileManager:
	def get_file_paths(path):
		return [
			y for x in os.walk(path)
			for y in glob(os.path.join(x[0], '*'))
			if os.path.isfile(y)
		]
		
	def open_file_readonly(path):
		return open(path, "r")
		
	def open_file_writeonly(path):
		return open(path, "w")