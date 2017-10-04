'''
Author: Nic Johnson

Title: migration-fuckery.py

Description:
	Comments/uncomments the bits of the util files that make
	makemigrations fail because tables and what not don't exist

History:
	November 02, 2016:
		-Date Created

'''
import os
import sys
import argparse as ap
import re

parser = ap.ArgumentParser(description="(Un)comments the bits that make makemigrations fail")
parser.add_argument("COMMAND", help="Which command to run", choices=["comment", "uncomment"])
parser.add_argument("-f", help="Only do the specified file", dest="FILE")
args = parser.parse_args()

comment = args.COMMAND.upper() == "COMMENT"
do_all = not args.FILE

if (do_all):
	files = [
		"apps/contribution/views/infographics_view.py",
	]
else:
	files = []
	files.append(args.FILE)

os.chdir("../")

start = re.compile(r'^\s?# *MIGRATION_FUCKERY')
end = re.compile(r'^\s?# *END_MIGRATION_FUCKERY')

for _file in files:
	try:
		f = open(_file)
		buff = f.readlines()
		f.close()
		new_buff = []
		lb = len(buff)
		i = 0
		startMatched = False
		flip = False
		for i in buff:
			i = i.rstrip()
			if (not startMatched):
				match = re.search(start, i)
			else:
				match = re.search(end, i)

			if (match and not startMatched):
				startMatched = True
				flip = True
				new_buff.append(i)
			elif (match and startMatched):
				startMatched = False
				flip = False
				new_buff.append(i)
			else:
				if (flip):
					if (comment):
						new_buff.append("#" + i)
					else:
						if (i[0] == "#"):
							new_buff.append(i[1:])
						else:
							new_buff.append(i)
				else:
					new_buff.append(i)

		f = open(_file, "w")
		for i in new_buff:
			f.write(i + "\n")
		f.close()
	except FileNotFoundError:
		print("ERROR: Can't open file " + _file)
		print("Exiting...")
		sys.exit(1)


















