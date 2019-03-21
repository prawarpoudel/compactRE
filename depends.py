import sys
import os
import os.path
import subprocess
from sys import platform

debug = False

class fileAttributes:
	def __init__(self,file_name=""):
		if file_name=="":
			print("Empty object created. No name provided. Please provide the name using function <object_name>.set_file_name(file_name)")
		self.attributes = set()
		self.file_name = file_name

	def set_file_name(self,file_name):
		print(f"Changing file_name from {self.file_name} to",end=" ")
		self.file_name = file_name
		print(f" {self.file_name}")

	def add_attributes(self,input_attributes):
		self.attributes.add(input_attributes)

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
			print(f"Child process terminated..")
		# read from the reading end of pipe
		my_reads = os.read(r,1000).decode('UTF-8').strip("\n")
		my_reads = my_reads.split(" ")
		if debug:
			print(f"Read from child process: {my_reads}")
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
	print(f"")

def parse_arguments(sysArgv):
	input_file_list = list()
	for idx,argument in enumerate(sysArgv[1:]):
		if debug:
			print(f"Operating on Command Argument {argument}")
		if argument[0]=="-" or argument[0]=="--":
			if debug:
				print(f"Detected - ")
			# flag mode, add others
			if argument[1:]=='h' or argument[1:]=='H' or argument[1:]=="help" or argument[1:]=="Help" or argument[1:]=="HELP":
				if debug:
					print(f"Detected {argument[1:]}")
				print_help_message()
				sys.exit(0)
			elif argument[1:]=='T' or argument[1:]=='t' or argument[1:]=="TEXT" or argument[1:]=="Text" or argument[1:]=="text":
				text_file = ""
				if debug:
					print(f"Detected {argument[1:]}")

				if not (len(sysArgv)>= idx+2):
					print("..Provided flag -t: No argument found for file name to read. Please use -h for help.")
					sys.exit(0)
				else:
					text_file = sysArgv[idx+2]
					if debug:
						print(f"File name to read the list is {text_file}.")
				if not os.path.isfile(text_file):
					print(f"File {text_file} not found.")
					sys.exit(0)
				if debug:
					print(f"File {text_file} found.")

				with open(text_file) as my_file:
					contents = my_file.read()				
					if debug:
						print(f"Content of file {text_file} read as:\n {contents}")
					input_file_list = contents.strip().split(" ")
				break
		elif argument=="xxxx":
			continue
		else:
			input_file_list = sysArgv[1:]

	return input_file_list