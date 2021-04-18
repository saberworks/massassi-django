from pprint import pprint

from django.utils import timezone
from django.utils.datetime_safe import datetime

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

        current_tz = timezone.get_current_timezone()

        for row in cursor.fetchall():
            self.stdout.write("Processing {}...".format(row['user_name']), ending='')

            reg_date = None

            if row['registration_date'] is not None:
                reg_date = datetime.strptime(str(row['registration_date']), "%Y-%m-%d %H:%M:%S")
                reg_date = current_tz.localize(reg_date)

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

            user.save(force_insert=True)

            self.stdout.write("Done")

        cursor.close()
        cnx.close()
