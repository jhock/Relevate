# Relevate Web App
 
### Useful Things

* Dump data from the database to json for easy set up
	* ```python3 manage.py dumpdata --indent 4 --exclude=contenttypes --exclude=auth.Permission -o base-data.json```
* Load that data back up
	* ```python3 manage loaddata base-data.json```
* When running tests, append apps.<_whatever_> after the command to avoid errors
	* Ex ```python3 manage.py test apps.profiles```
* Running manual manage.py commands on AWS
	* ````cd /opt/python/current/app/````
	* ````/opt/python/run/venv/bin/python manage.py <command>````
* Populating local database with universities information
	*   sh populate_university_table.sh or python manage.py insert_university_list_into_table
* Redo the database from scratch script
	* ``` MAKE SURE YOU ARE IN THE SCRIPT DIRECTORY WHEN YOU RUN THE SCRIPT located in relevate_web_app/scripts```
	*  ``` Run this script --  "sh redo_database.sh" ```
	*  ``` Run this script --  "sh redo_database_py3_explicit.sh" if your run manage.py with python3 ``` 
	*  ``` This takes care of redumping old data, if you have a base-data.json as described above. ```
	*  ``` This takes care populating university listings ```
* Create the database for the first time
	* ``` Run this script -- "sh createdb.sh relevate_dev_db rel_user relevate_dev_pass"  found in relevate_web_app/script ```
* Building the docs 
	* Fill in this template
	````
	<Page Title> Documentation
	===============================

	.. toctree::
	   :maxdepth: 2
	   :caption: Contents:

	.. automodule :: <path.to.the.module>
		:members:
	````
	* Add the file you just made to index.txt
	````
		Adviser Views <advisers/adviser_views>
		Adviser Models <advisers/adviser_models>
		MyShittyFile <path/to/MyShittyFile>
	````
	* cd into docs directory
	* run ```make html```
