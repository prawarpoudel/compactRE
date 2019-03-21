import sys
import os
import os.path
import subprocess
import depends
from sys import platform

debug = depends.debug

if __name__=="__main__":
	os_type=depends.check_platform()

	if(len(sys.argv)<2):
		print(f"Provide at least a file name for analysis.")
		print(f"Use -h flag for help message")
		sys.exit(0)

	input_file_list = depends.parse_arguments(sys.argv)

	if debug:
		print(f"The file to reverse engineer are: {input_file_list}")
	my_attribute_dict = depends.generate_attribute_dict(input_file_list)

	if debug:
		print(f"Done generating attributes!!\n\t..Check following..")
	depends.print_dict(my_attribute_dict)