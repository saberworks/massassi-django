#!/bin/bash
set -euxo pipefail

source ./database_info.sh

# WIPE DATABASE
#find ../ -path '*/migrations/*' -regex ".*/[0-9]+.*" -delete
#find ../ -name '*.pyc' -delete
#
#dropdb -h localhost -p 5432 -U massassi massassi
#createdb -h localhost -p 5432 -U massassi --owner=massassi massassi
#sudo -u postgres dropdb massassi
#sudo -u postgres createdb --owner=massassi massassi

# REBUILD DATABASE
python ../manage.py makemigrations users
python ../manage.py makemigrations
python ../manage.py migrate

# DELETE EVERYTHING IN media/
rm -rf ../media/*

# IMPORT EVERYTHING
./import_users.sh
./import_sotd.sh
./import_level_categories.sh
./import_levels.sh
./import_level_comments.sh
./import_level_ratings.sh
./import_lotw.sh
./import_news.sh
./import_holiday_logos.sh

# SET SEQUENCES
python ../manage.py sqlsequencereset users sotd levels news | python ../manage.py dbshell
