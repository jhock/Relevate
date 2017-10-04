# Relevate Web App

### Overview

Relevate is a content creation platform for research backed relationship articles. The goal is to 
make the research done by professionals available to the general public. The project has evolved 
into a desktop site for users to consume content, and contributors to create content. A mobile app
and api are planned for development, which will be used solely by the general public to have easy
access to the information (no functionailty for contributors). The desktop site will re-direct to
a link for mobile users to download the mobile app when it is completed; the web app is not structured
for use on smaller screens, and there are no plans for smaller screen compatibility to be added.

The requirements for this project are python3, django, and mysql and is running on Amazon's AWS service.

The most important account for the web app is "relevate@outlook.com". This account has privledges that 
other accounts do not, such as the ability to see all posts, while a regular contributor can only see the ones
they have posted. It is also used by the Relevate team to post their own content. Currently the view will
check to see if the user's email is "relevate@outlook.com", and if it is, grant them access. This may be replaced
in the future by a list of users set as "staff", and provide all staff members with access. Check accounts_and_passwords.txt
for the "relevate@outlook.com" password.

-----------About Content Creation------------------------------
In addition to providing research backed relationship articles to the public, the Relevate team also wants to
be a resource for showing professionals how to create quality content for their users on mediums such as videos, books,
articles, social media, and podcasts. This section is not viewable for general users, only for contributors. All content is
currently posted by the "relevate@outlook.com" account, but again this can be changed to a staff list.

### Use Case Walkthrough

A user visits the site and signs up for an account.

> Currently email confirmation is disabled, however the skeleton for using SendGrid is there. The value _auto__confirm_
> can be changed to turn email confirmation on or off. True turns it off, and False turns it on.

The user then can sign up to be a contributor. If the highest degree the contributor has 
completed is either a Student-Undergraduate or Student-Masters, the contributor must have a
mentor. Each contributor must also specify expertise topics for themselves. These are the areas that 
the contributor feels they are qualified to write about.

> Currently the process to approve the contributor is disabled for the beta test. Typically
> the contributors application would go into a Pending Contributors queue to be approved by 
> a staff member.

Once a contributor's application has been approved, they can now post content. This includes article,
links to outside sites, and infographics. These posts are also tagged by the contributor, using
the same choices of tags that they were presented when creating their account.
If the contributor was required to have a mentor, their mentor will approve/deny the contributors posts before they go
live. 



### Installing/Running

_Note: You must use Python 3 to run this project_

To run a local copy of Relevate, first clone this repo. Next, you must download the required dependencies via

````
pip install -r requirements.txt
````

Once that completes, run the following command from the top level of the repository:

````
python manage.py runserver
````

Then navigate to `localhost:8000` in a web browser.



### Setting Up and Connecting to Database

There are two MYSQL databases used for development: local and "beta" (located on AWS RDS) databases. Settings for these are located in
<relevate_web_app/setting/local.py> and <relevate_web_app/setting/beta.py>. In order to switch the database you are using, change
_os.environ.setdefault_ in BOTH <manage.py> and <wsgi.py> to _settings.local_ or _settings.beta_.

-------Beta-----------
IMPORTANT: THE BETA DATABASE HAS ARTICLES, POSTS, AND USER PROFILES WHICH SHOULD NOT BE DELETED. BE CAREFUL MESSING WITH THIS. IT IS ONLY
TO BE USED FOR ALPHA AND BETA TESTING.

Beta database is located at aabfsxdo8won4f.czggqranenuo.us-west-2.rds.amazonaws.com on port 3306. _database__user_ and _database__password_
are stored in <relevate_web_app/settings/access_keys.py> ACCESS_KEYS IS NOT INCLUDED IN GIT. IF YOU ARE MISSING THIS FILE, CONTACT SOMEONE WHO
HAS IT.

The easiest way to update "beta" database is by changing _settings.local_ to _settings.beta_ and running the following commands:

	python manage.py makemigrations

	python manage.py migrate 

--------Local--------
This is the local database on your personal computer that is used for development without having to mess with the live "beta" database.
Several scripts for database set-up and management are included in <relevate_web_app/scripts>. 

-Setting up local database:
Step 0: If you have not set up a local MYSQL server on your machine yet, follow the steps here: https://dev.mysql.com/doc/mysql-getting-started/en/

Step 1: Create the database by running the following script in <relevate_web_app/scripts>:

	./createdb.sh relevate_dev_db relevate_user relevate_dev_pass

which will create a new MYSQL database _relevate_dev_db_ on 'localhost' with user _relevate_user_ and password _relevate_dev_pass_.

Step 2: Now that you have an empty database, you can add the tables and fields for the models. To do this, run the following commands:

	python manage.py makemigrations

	python manage.py migrate

Remember, if you are switching between using "local" and "beta" databases, the migrations files may not necessarily line up. If you have
issues with this step or issues with migrations in the future, please read up on migrations on these links:
	https://docs.djangoproject.com/en/1.11/topics/migrations/
	https://realpython.com/blog/python/django-migrations-a-primer/
	https://simpleisbetterthancomplex.com/tutorial/2016/07/26/how-to-reset-migrations.html

Step 3: By this step, you should hopefully have a database _relevate_dev_db_ on 'localhost' with all tables and fields needed. There are
two final things you must do, which are to poulate the degree and university tables. These tables contain lists of degrees and universities
that contributors can select to fill in their credentials. To do this, run the two scripts at <relevate_web_app/scripts>:

	./populate_degree_table.sh

	./populate_university_table.sh

Congratulations! You have a working local database you can use for testing and development without disrupting the "beta" database.

One final note: redo__database.sh in <relevate_web_app/scripts> can be used if you run into major issues with migrations. It will
delete the migration files and make a fresh migration to the database.



### Managing the Live Site Using Amazon Web Services

The relevate web app, "beta" database, and api are hosted on Amazon Web Services. To sign in, go to 
https://relevatedev.signin.aws.amazon.com/console, click sign in as root, and enter the Main Account Email and Main Account Password from 
the <accounts-and-passwords.txt> file.

Deployment of a new build is done through Elastic Beanstalk. You can deploy using the eb web console page, but it is more time consuming and
a lot of configuration is not available. The best way to deploy is with the eb command line interface or CLI. Learn how to install,
configure, and deploy a new build using CLI here: http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3.html
There are several environments, but the main one is "beta" which we use for alpha and beta testing with the contributors. 
Once it is installed you can simply deploy from the root project folder using the commands:

Initialize eb:

	eb init

make sure you are deploying to the right environment:

	eb list

Change environment if it is not the right one, switch environments:

	eb use _environment-name_

Deploy:

	eb deploy

Note: if someting does wrong with deployment, the console at https://us-west-2.console.aws.amazon.com/elasticbeanstalk/home gives better
logs and monitoring than you can get through the command line.



### API

Django REST API framework will be used to serve information from the database to the app and is under development. The api project
folder is under <relevate_web_app/apps/api>. The information that the api will process is user profiles and posts. All that is needed
for REST framework is djangorestframework, installed by the following command:

	pip install djangorestframework

More information and documentation here: http://www.django-rest-framework.org



### App

Ionic app prototypes are located in <mobile-app/Prototypes>.


### Maintaining Documentation

Sphinx is used for an easy to use and read documentation and provides an in-depth description of Models, Forms, Views, and Utilities. 
Sphinx creates linked HTML documents by searching for comments in the .py files which are surrounded by ''' '''. To view these documents,
open the file <relevate_web_app/docs/_build/html/index.html>.

How to create Sphinx documentation:

Step 0: You must install Sphinx before you can make a new set of linked html documents for the Relevate code. Follow the steps here:
http://www.sphinx-doc.org/en/stable/install.html 
to install it. 

Step 1: Go to the .py file that you want to create documentation for. Type ''' under a class or function and fill it in with a description
of what it is and what purpose it serves. A _:param:_ and _:return:_ line will be automatically inserted for each parameter and return value.
Enter in what each parameter and return value are.

Step 2: Navigate to <relevate_web_app/docs>. here you will see multiple folders such at "advisers", "articles", and "posts", all containing
text files such as "adviser_models.txt" and "adviser_views.txt". The txt files tell Sphinx where to look in the project for documentation.
Add the location of the documentation you added in Step 1 to an existing txt file, or create a new on in the proper folder and add it. See
http://www.sphinx-doc.org/en/stable/tutorial.html for more info.

Step 3: Open <docs/index.txt> and add the location of the txt file if you created a new one. This will create a link on the index page to your
documentation. For example, if you edited <docs/authentication/authentication_views.txt>, you would add the line 
"Authentication Views <authentication/authentication_views>".

Step 4: Run the following command in </docs> to make the documentation:

	make html

Note: Some existing code does not have documentation yet. If you see something without it, add it.

For general documentation, add to this README.



### Future Work

- [ ] Dynamically add entries to various tabs on the About Us page
- [ ] Have a request system for new tags, similar to how contributor applications/posts
are approved denied
- [ ] Finish the mobile app API



### Useful Things

* Dump data from the database to json for easy set up
	* ```python manage.py dumpdata --indent 4 --exclude=contenttypes --exclude=auth.Permission -o base-data.json```
* Load that data back up
	* ```python manage.py loaddata base-data.json```
* When running tests, append apps.<_whatever_> after the command to avoid errors
	* Ex ```python manage.py test apps.profiles```
* Running manual manage.py commands on AWS
	* ````cd /opt/python/current/app/````
	* ````/opt/python/run/venv/bin/python manage.py <command>````
* Redo the database from scratch script (bash)
	* ``` MAKE SURE YOU ARE IN THE SCRIPT DIRECTORY WHEN YOU RUN THE SCRIPT located in relevate_web_app/scripts```
	*  ``` Run this script --  "sh redo_database.sh" ```
	*  ``` Run this script --  "sh redo_database_py3_explicit.sh" if your run manage.py with python3 ``` 
	*  ``` This takes care of redumping old data, if you have a base-data.json as described above. ```
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

	.. module :: <path.to.the.module>
	.. autoclass :: <class name>
		:members:
	````
	* Add the file you just made to index.txt
	````
		Adviser Views <advisers/adviser_views>
		Adviser Models <advisers/adviser_models>
		MyFile <path/to/MyFile>
	````
	* cd into docs directory
	* run ```make html```



### People who have contributed to this project
	- Joshua Hock - email: joshua.a.hock@gmail.com
	- Uzzi Emuchay
	- Nic Johnson

	The Relevate project has been developed under guidance by the Relevate team at Kansas State University.
	Current Relevate Team members and positions as of 9/2017:

	-Co-Director: Amber Vennum
	-Co-Director: Natalie Pennington
	-Assistant Director: Stacy Conner
	-Special Operations:
		Michelle Busk
		Denzel Jones
		Eric Goodcase
		Jeremy Kanter
		Loren Taylor
		Morgan Bialas			

