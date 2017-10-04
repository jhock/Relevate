#!/usr/bin/env bash


MYSQL=`which mysql`

Q1="REPLACE INTO degree (abbreviation, name) VALUES
    ('AA', 'Associate of Arts'),
            ('AS', 'Associate of Science'),
            ('AAS', 'Associate of Applied Science'),
            ('BA', 'Bachelor of Arts'),
            ('BS', 'Bachelor of Science'),
            ('BFA', 'Bachelor of Fine Arts'),
            ('BAS', 'Bachelor of Applied Science'),
            ('MA', 'Master of Arts'),
            ('MS', 'Master of Science'),
            ('MBA', 'Master of Business Administration'),
            ('MFA', 'Master of Fine Arts'),
            ('Ph', 'Ph.D.'),
            ('JD', 'J.D. (Law Degree)'),
            ('MD', 'Doctor of Medicine'),
            ('DDS', 'Doctor of Dental Surgery');"
Q2="use relevate_dev_db;"
SQL="${Q2}${Q1}"

$MYSQL -u root -p -e "$SQL"

mysql -u root relevate_dev_db -p < ../Insert_MyRelevate_Topics.sql
