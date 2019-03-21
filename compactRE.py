import sys
import os
import os.path
import subprocess
import depends
from sys import platform

debug = depends.debug

if __name__=="__main__":

	my_attribute_dict = dict()
	util_list = ["file","nm"]

	os_type=depends.check_platform()

	if(len(sys.argv)<2):
		print(f"Provide at least a file name for analysis.")
		print(f"Use -h flag for help message")
		sys.exit(0)

	input_file_list = depends.parse_arguments(sys.argv)

	if debug:
		print(f"The file to reverse engineer are: {input_file_list}")

	for files in input_file_list:
		if files=="":
			print(f"W: File name is empty")
			continue
		elif not os.path.isfile(files):
			print(f"W: File {files} not found")
			continue

		my_attribute_dict[files] = depends.fileAttributes(files)
		for util in util_list:
			if debug:
				print(f"Running utility \'{util}\' on file \'{files}\'..")
			attrib_now = depends.run_file(util,files)
			if debug:
				print(f"The attributes determined are: {attrib_now}")
			for each_attribute in attrib_now:
				my_attribute_dict[files].add_attributes(each_attribute.strip('\\n\''))
