from users.models import User
from massassi.util import OurBaseCommand

class Command(OurBaseCommand):
    help = 'Imports users from mysql database'

    # CREATE TABLE IF NOT EXISTS "auth_user" (
    # "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    # "password" varchar(128) NOT NULL,
    # "last_login" datetime NULL,
    # "is_superuser" bool NOT NULL,
    # "username" varchar(150) NOT NULL UNIQUE,
    # "email" varchar(254) NOT NULL,
    # "is_staff" bool NOT NULL,
    # "is_active" bool NOT NULL,
    # "date_joined" datetime NOT NULL,

    def handle(self, *args, **options):
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
