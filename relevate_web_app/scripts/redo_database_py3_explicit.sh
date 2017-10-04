#!/usr/bin/env bash

python3 ../manage.py dumpdata --indent 4 --exclude=contenttypes --exclude=auth.Permission -o base-data.json

MYSQL=`which mysql`

Q1="DROP DATABASE relevate_dev_db;"
SQL="${Q1}"
$MYSQL -u root -p -e "$SQL"

sh createdb.sh relevate_dev_db rel_user relevate_dev_pass

rm -f ../apps/contribution/migrations/*
rm -f ../apps/profiles/migrations/*
touch ../apps/profiles/migrations/__init__.py
touch ../apps/contribution/migrations/__init__.py
python3 ../manage.py makemigrations
python3 ../manage.py migrate

python3 ../manage.py loaddata base-data.json
mv base-data.json ../../relevate_web_app/
sh populate_university_table.sh