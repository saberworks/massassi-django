source ./database_info.sh
python ../manage.py import_holiday_logos --mysql_host $MYSQL_HOST --mysql_user $MYSQL_USER --mysql_pass $MYSQL_PASSWORD --mysql_db $MYSQL_DATABASE --older_files_path /home/brian/code/massassi-django/import/holiday_logos/older --newer_files_path /home/brian/code/massassi-django/import/holiday_logos/newer
