source ./database_info.sh
python ../manage.py import_users --mysql_host $MYSQL_HOST --mysql_user $MYSQL_USER --mysql_pass $MYSQL_PASSWORD --mysql_db $MYSQL_DATABASE
echo "resetting sequences...\n";
python ../manage.py sqlsequencereset users | python ../manage.py dbshell
python ../manage.py import_staff --mysql_host $MYSQL_HOST --mysql_user $MYSQL_USER --mysql_pass $MYSQL_PASSWORD --mysql_db $MYSQL_DATABASE
