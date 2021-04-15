from pprint import pprint

from django.core import management
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django.utils import timezone

from users.models import User
from massassi.util import OurMySqlImportBaseCommand

class Command(OurMySqlImportBaseCommand):
    help = 'Imports users from mysql database'

    def handle(self, *args, **kwargs):
        self.import_users(*args, **kwargs)

    def import_users(self, *args, **options):
        cnx = super().get_connection(options)

        cursor = cnx.cursor(dictionary=True)

        query = "SELECT * FROM users ORDER BY user_id"

        cursor.execute(query)

        for row in cursor.fetchall():
            reg_date = row['registration_date'] if row['registration_date'] else None

            user = User(
                id=row['user_id'],
                username=row['user_name'],
                email=row['user_email'],
                is_superuser=row['user_id'] == 1,
                is_staff=row['user_id'] == 1,
                password=row['user_password'],
                date_joined=reg_date,
                is_active=True,
            )

            user.save()

            self.stdout.write("Processed {}".format(row['user_name']))

        cursor.close()
        cnx.close()
