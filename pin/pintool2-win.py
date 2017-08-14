#!/usr/bin/env python
#coding: utf8 
#
#prog_name= 'pintool2.py'
#prog_version = '2.0'
#prog_release = '20160724'
#prog_author = 'Sebastien Damaye'
#prog_author_mail = 'sebastien.damaye@gmail.com'

"""
pintool2 is an improved version of the pintool.py script written by wagiro (Eduardo García),
available here (https://github.com/wagiro/pintool).

This version integrates an additional reverse order option to brute force password in reverse order (starts from the end).

This tool can be useful for solving some reversing challenges in CTFs events.
Implements the technique described here (http://shell-storm.org/blog/A-binary-analysis-count-me-if-you-can/). 
"""

import sys
import string as s
import subprocess
import argparse
import re
from subprocess import PIPE, Popen

#configure by the user
PINBASEPATH = "c:/pin"
PIN = "%s/pin.exe" % PINBASEPATH
#INSCOUNT32 = "%s/source/tools/ManualExamples/obj-ia32/inscount0.so" % PINBASEPATH
#INSCOUNT64 = "%s/source/tools/ManualExamples/obj-intel64/inscount0.so" % PINBASEPATH
INSCOUNT32 = "c:/tools/inscount0.dll"
INSCOUNT64 = INSCOUNT32


def start():
	
	parser = argparse.ArgumentParser(prog='pintool2.py')
	parser.add_argument('-e', dest='study', action='store_true', default=False, help='Study the password length, for example -e -l 40, with 40 characters')
	parser.add_argument('-l', dest='len', type=str, nargs=1, default='10', help='Length of password (Default: 10 )')
	parser.add_argument('-c', dest='number', type=str, default=1, help="Charset definition for brute force\n (1-Lowercase,\n2-Uppecase,\n3-Numbers,\n4-Hexadecimal,\n5-Punctuation,\n6-All)")
	parser.add_argument('-b', dest='character', type=str, nargs=1, default='', help='Add characters for the charset, example -b _-')
	parser.add_argument('-a', dest='arch', type=str, nargs=1, default='32', help='Program architecture 32 or 64 bits, -a 32 or -a 64 ')
	parser.add_argument('-i', dest='initpass', type=str, nargs=1, default='', help='Inicial password characters, example -i CTF{')
	parser.add_argument('-s', dest='simbol', type=str, nargs=1, default='_', help='Simbol for complete all password (Default: _ )')
	parser.add_argument('-d', dest='expression', type=str, nargs=1, default='!= 0', help="Difference between instructions that are successful or not (Default: != 0, example -d '== -12', -d '=> 900', -d '<= 17' or -d '!= 32')")
	parser.add_argument('-r', dest='reverse', action='store_true', default=False, help='Start in reverse order')
	parser.add_argument('Filename',help='Program for playing with Pin Tool')


	if len(sys.argv) < 2:
		parser.print_help()
		print ("")
                print ("Examples:")
                print ("  ./pintool2.py -l 30 -c 1,2,3 -b _{} -s - baleful")
		print ("  ./pintool2.py -l 37 -c 4 -i CTF{ -b }_ -s - -d '=> 651' reverse400")
		print ("  ./pintool2.py -c 1,2,3 -b _ -s - -a 64 -l 28 wyvern")
		print ("  ./pintool2.py -r -l 32 -c 1,2,3 -b _{$} -s - 01f47d58806a8264cd4b2b97b9dabb4a")
		print ("")
		sys.exit()
	
	args = parser.parse_args()

	return args


def getCharset(num,addchar):
	char = ""
	charset = { '1': s.ascii_lowercase, 
				'2': s.ascii_uppercase,
				'3': s.digits,
				'4': s.hexdigits,
				'5': s.punctuation,
				'6': s.printable}
	

	if num is 1:
		return charset['1']
	else:
		num = num.split(',')

	for i in num:
		if 1 <= int(i) <= 6:
			i= '%s' % i
			char += charset[i]
		else:
			print "Number %s out of range." % (i)

	return char+''.join(addchar)


def pin(passwd):
	try:		
		PIN_PATH = "c:/pin/pin.exe"
		PIN_TOOL = "c:/tools/inscount0.dll"
		TOOL_ARG = "-t"
		DASH_ARG = "--"
		TARGET_BIN = args.Filename
		
		p = subprocess.Popen([PIN_PATH, TOOL_ARG, PIN_TOOL, DASH_ARG, TARGET_BIN], stdin=PIPE, stdout=PIPE)
		p.communicate("%s\n" % passwd)[0]
		
		output = subprocess.check_output(["more", "inscount.out"], shell=True)
	except:
		print "Unexpected error:", sys.exc_info()[0]
		raise

	output = re.findall(r"Count ([\w.-]+)", output)

	return int(''.join(output))


def lengthdetect(passlen):
	inicialdifference = 0
	for i in range(1,passlen+1):
		password = "_"*i
		inscount = pin(password)
		
		if inicialdifference == 0:
			inicialdifference = inscount

		print "%s = with %d characters difference %d instructions" %(password, i, inscount-inicialdifference)


def solve(initpass,passlen,symbfill,charset,expression,reverse):
	
	initlen = len(initpass)
	
	for i in range(initlen,passlen):
		
		tempassword = initpass + symbfill*(passlen-i)
		inicialdifference = 0

		for char in charset:
			
			password = tempassword[:i] + char + tempassword[i+1:]
			if reverse:
				password = password[::-1]
			
			inscount = pin(password)
			
			if inicialdifference == 0:
				inicialdifference = inscount

			difference = inscount-inicialdifference

			print "%s = %d difference %d instructions" %(password.replace("\\","",1), inscount, difference)
			

			if "!=" in expression:
				if difference != int(number):
					print "%s = %d difference %d instructions" %(password.replace("\\","",1), inscount, difference)
					initpass += char
					break
			elif "==" in expression:
				if difference == int(number):
					print "%s = %d difference %d instructions" %(password.replace("\\","",1), inscount, difference)
					initpass += char
					break
			elif "<=" in expression:
				if difference <= int(number):
					print "%s = %d difference %d instructions" %(password.replace("\\","",1), inscount, difference)
					initpass += char
					break
			elif "=>" in expression:
				if difference >= int(number):
					print "%s = %d difference %d instructions" %(password.replace("\\","",1), inscount, difference)
					initpass += char
					break
			else:
				print "Unknown value for -d option"
				sys.exit()

			if char == charset[-1]:
				print "\n\nPassword not found, try to change charset...\n"
				sys.exit()	
	
	
	return password.replace("\\","",1)


if __name__ == '__main__':

	args = start()

	initpass = ''.join(args.initpass)
	passlen = int(''.join(args.len))
	symbfill = ''.join(args.simbol)
	charset = symbfill+getCharset(args.number,args.character)
	arch = ''.join(args.arch)
	expression = ''.join(args.expression).rstrip()
	number = expression.split()[1]
	study = args.study
	reverse = args.reverse

	if len(initpass) >= passlen:
		print "The length of init password must be less than password length."
		sys.exit()


	if passlen > 64:
		print "The password must be less than 64 characters."
		sys.exit()


	if len(symbfill) > 1:
		print "Only one symbol is allowed."
		sys.exit()


	if arch == "32":
		INSCOUNT = INSCOUNT32
	elif arch == "64":
		INSCOUNT = INSCOUNT64
	else:
		print "Unknown architecture"
		sys.exit()


	if study is True:
		lengthdetect(passlen)
		sys.exit()


	password = solve(initpass,passlen,symbfill,charset,expression,reverse)

	print "Password: ", password