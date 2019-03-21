import sys
import os
import os.path
import subprocess
from sys import platform

debug = False

# we have three kinds of atributes, so a list of three sets
# 0: info, 1: imported function, 2: dynamically loaded libs. add more if needed
# change to be made in class fileAttributes also
util_list = [["file"],["nm"],["ldd"]]

os_type = "dont_know"

class fileAttributes:
	def __init__(self,file_name=""):
		if file_name=="":
			print("Empty object created. No name provided. Please provide the name using function <object_name>.set_file_name(file_name)")
		# we have three kinds of atributes, so a list of three sets
		# 0: info, 1: imported function, 2: dynamically loaded libs
		self.attributes = [set() for i in range(len(util_list))]
		self.file_name = file_name

	def set_file_name(self,file_name):
		print(f"..Changing file_name from {self.file_name} to",end=" ")
		self.file_name = file_name
		print(f" {self.file_name}")

	def add_attributes(self,attribute_id,input_attributes):
		self.attributes[attribute_id].add(input_attributes)

	def print_attributes(self):
		print(f"Printing attributes for file {self.file_name}")
		for idx,each_attribute_kind in enumerate(self.attributes):
			print(f".. attributes as result of {util_list[idx]} follows:")
			for each_attribute in each_attribute_kind:
				print(f".... {each_attribute}")

def check_platform():
	os_type = "dont_know"
	if platform == "linux" or platform == "linux2":
	    if debug:
	        print(f"Found Linux System: {platform}\n")
	    os_type = "linux"
	elif platform == "darwin":
	    if debug:
	        print(f"Found Mac OS X: {platform}\n")
	    os_type = "mac"
	elif platform == "win32":
	    if debug:
	        print(f"Found windows System: {platform}")
	    os_type = "windows"
	else:
	    if debug:
	        print(f"Could not determine the OS type")

	return os_type

# Following code runs the first of the tools that we want to integrate
def run_file(command,subject_file):
	# let us create pipe() and write to the write end of pipe from child and read from parent
	r,w = os.pipe()
	my_reads = ""
	my_pid = os.fork()

	dev_null_file_id = os.open(os.devnull,os.O_WRONLY)
	if debug:
		print(f"DEV NULL file ID is {dev_null_file_id}")

	if my_pid<0:
		print(f"Error in forking child inside function run_file({command},{subject_file})..")
		sys.exit(0)
	elif my_pid>0:
		# close the writing end of pipe here
		os.close(w)
		# this is parent process
		if debug:
			print(f"Forked child process {my_pid} for \'file\' operation")	
			print("Parent waiting..")
		# wait for the child process to complete
		os.wait()	
		if debug:
			print(f"..Child process terminated..")
		# read from the reading end of pipe
		my_reads = os.read(r,1000).decode('UTF-8').strip("\n")
		my_reads = my_reads.split(" ")
		if debug:
			print(f"..Read from child process: {my_reads}")
	else:
		os.close(r)
		os.dup2(w,1)
		os.dup2(dev_null_file_id,2)
		my_arguments = [command]+subject_file.split(" ")
		os.execvp(command,my_arguments)
		print(f"Should not be here, but here I am..")
	return my_reads

def print_help_message():
	print(f"Help Message for CompactRE:")
	print(f"usage: compactRE.py [filename <filename2>..] [-t textFileName.txt] [-h]")
	print(f"-t textFileName.txt: \tReads the file names from file textFileName.txt")
	print(f"-h: \tPrint help messages")
	print(f"-d: \t[True or False] \t Enable or disable debug messages")
	print(f"")

def parse_arguments(sysArgv):
	global debug
	input_file_list = list()

	if debug:
		print(f"Parsing command line argument")
	# join all the elements in arguments separated by <space>
	sys_arg = " ".join(sysArgv[1:]).strip()
	# now break them by - sign
	sys_arg_broken = sys_arg.split("-")

	# things should be in place now
	for each_arg in sys_arg_broken:
		each_arg_broken = each_arg.split(" ")
		if each_arg_broken[0] == 'h' or each_arg_broken[0] == 'H':
			if debug:
				print(f"..Detected help command: {each_arg_broken[0]}")
			print_help_message()
			sys.exit(0)
		elif each_arg_broken[0] == 'd' or each_arg_broken[0] == 'D':
			debug = str(each_arg_broken[1].strip())=="True"
			print(f"debug changed to {debug}")
		elif each_arg_broken[0] == 't' or each_arg_broken[0] ==  'T':
			if debug:
				print(f"..Detected text file command: {each_arg_broken[0]}")
			if len(each_arg_broken)<2:
				print(f"..No file provided with \'{each_arg_broken[0]}\' argument")
				sys.exit(0)
			if not os.path.isfile(each_arg_broken[1]):
				print(f"..File \'{each_arg_broken[1]}\' not found")
				sys.exit(0)
			with open(each_arg_broken[1]) as my_file:
				contents = my_file.read()
				if debug:
					print(f"....Content of file {each_arg_broken[1]} read as:\n{contents}")
				input_file_list = contents.strip().split("\n")
			break
		else:
			for each_file in each_arg_broken:
				if not each_file=="":
					input_file_list.append(each_file)
	return input_file_list


def print_dict(input_dict):
	for this_key in input_dict.keys():
		print(f"For file:\'{this_key}\':")
		input_dict[this_key].print_attributes()

def is_tool(name):
    """Check whether `name` is on PATH and marked as executable."""
    # from whichcraft import which
    from shutil import which
    return which(name) is not None

def generate_attribute_dict(input_file_list,util_list):
	my_attribute_dict = dict()
	for idx,util_list_internal in enumerate(util_list):
		util_list_temp = list()

		for util in util_list_internal:
			if is_tool(util):
				util_list_temp.append(util)
			else:
				if debug:
					print(f"..utility {util} not installed in system")
		for file in input_file_list:
			if file=="":
				print(f"W: file name is empty")
				continue
			elif not os.path.isfile(file):
				print(f"W: file {file} not found")
				continue

			if file not in my_attribute_dict.keys():
				if debug:
					print(f"..adding {file} to dictionary")
				my_attribute_dict[file] = fileAttributes(file)
			for util in util_list_temp:
				if debug:
					print(f"..Running \'{util}\' on file \'{file}\'")
				attrib_now = run_file(util,file)
				if debug:
					print(f"..the attributes determined are: {attrib_now}")
				for each_attribute in attrib_now:
					my_attribute_dict[file].add_attributes(idx,each_attribute.strip('\\n\''))

	return my_attribute_dict