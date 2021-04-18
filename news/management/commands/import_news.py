from functools import lru_cache

import pytz
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datetime_safe import datetime

from massassi.util import OurMySqlImportBaseCommand

from news.models import News
from users.models import User


class Command(OurMySqlImportBaseCommand):
    help = 'Imports news from mysql database'

    def handle(self, *args, **options):
        self.import_news(*args, **options)

    def import_news(self, *args, **options):
        cnx = self.get_connection(options)

        cursor = cnx.cursor(dictionary=True)

        query = """
            SELECT *
              FROM massassi_news mn
              JOIN massassi_staff ms ON mn.user_id = ms.user_id
          ORDER BY mn.post_id
        """

        cursor.execute(query)

        for row in cursor.fetchall():
            self.stdout.write("Processing post {}...".format(row['headline']), ending='')

            user = get_staff_user(row['user_name'])
            if not user:
                self.stderr.write("unable to find user {}".format(row['user_id']))
                continue

            date_posted = datetime.fromtimestamp(
                row['time'], tz=pytz.timezone('America/Los_Angeles')
            )

            post = News(
                id=row['post_id'],
                user=user,
                headline=row['headline'],
                story=row['story'],
                date_posted=date_posted,
            )

            post.save(force_insert=True)

            self.stdout.write("Done")

        cursor.close()
        cnx.close()


# Note that all users and staff members must be imported first using:
#   python manage.py import_users
@lru_cache(maxsize=None)
def get_staff_user(staff_user_name):
    try:
        return User.objects.get(username=staff_user_name)
    except ObjectDoesNotExist:
        return None
