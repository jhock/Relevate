"""
Converts a list of Universities from a csv file to python tuple. 
Need this script in case we get more extensive universities csv file
given to us through the medium of a csv.
Writes output to a python file located in the same directory
"""
import csv
from sys import argv
script, csv_file_name, output_python_file = argv
print("Converting %s of university listing to tuple. \n" % csv_file_name)


with open(csv_file_name) as csv_file:
	reader = csv.DictReader(csv_file)
	tr = open(output_python_file, 'w')
	name_of_dic = "WORLD_UNIVERSITIES_LISTS = [\n"
	print("Writing to %s or creating file then writing to it if it doesn't exist. \n" % output_python_file)
	tr.write(name_of_dic)
	for row in reader:
		if row["Country Abbreviation"] == "US":
			university_ = row['Name of University'].replace('"', "")
			finish_prod = university_.replace("'", "’")
			tr.write('	"%s",\n' % finish_prod)
	end_line = "]\n"
	tr.write(end_line)
print("Tasks Complete!\n")
