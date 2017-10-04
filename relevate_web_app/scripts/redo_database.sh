#!/usr/bin/env bash

python ../manage.py dumpdata --indent 4 --exclude=contenttypes --exclude=auth.Permission -o base-data.json

MYSQL=`which mysql`

Q1="DROP DATABASE relevate_dev_db;"
SQL="${Q1}"
$MYSQL -u root -p -e "$SQL"

sh createdb.sh relevate_dev_db rel_user relevate_dev_pass

rm -f ../apps/contribution/migrations/*
rm -f ../apps/profiles/migrations/*
touch ../apps/profiles/migrations/__init__.py
touch ../apps/contribution/migrations/__init__.py
python ../manage.py makemigrations
python ../manage.py migrate

python ../manage.py loaddata base-data.json
mv base-data.json ../../relevate_web_app/
sh populate_university_table.sh
