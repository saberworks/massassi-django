source ./database_info.sh
python ../manage.py import_sotd --mysql_host $MYSQL_HOST --mysql_user $MYSQL_USER --mysql_pass $MYSQL_PASSWORD --mysql_db $MYSQL_DATABASE --ss_path /home/brian/code/massassi-django/import/sotd/
