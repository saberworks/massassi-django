from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from users.models import User
from massassi.util import OurMySqlImportBaseCommand

class Command(OurMySqlImportBaseCommand):
    help = 'Imports users from mysql database'

    def handle(self, *args, **kwargs):
        self.import_users(*args, **kwargs)
        self.import_staff(*args, **kwargs)

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

    def import_staff(self, *args, **options):
        cnx = super().get_connection(options)

        cursor = cnx.cursor(dictionary=True)

        query = "SELECT * FROM massassi_staff ORDER BY user_id"

        cursor.execute(query)

        for row in cursor.fetchall():
            user = get_user(row['user_name'])

            if user:
                user.is_staff = True;
                user.save()
            else:
                user = User(
                    username=row['user_name'],
                    email=row['user_email'],
                    is_superuser=False,
                    is_staff=True,
                    password=row['password'],
                    date_joined=timezone.now(),
                    is_active=True,
                )

                user.save()

            self.stdout.write("Processed {}".format(row['user_name']))

        cursor.close()
        cnx.close()


def get_user(user_name):
    try:
        user = User.objects.get(username=user_name)
    except ObjectDoesNotExist:
        user = None

    return user
