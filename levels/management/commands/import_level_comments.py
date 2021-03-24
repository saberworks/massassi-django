import pytz

from django.core.exceptions import ObjectDoesNotExist
from django.utils.datetime_safe import datetime
from django.utils.html import strip_tags

from users.models import User
from levels.models import LevelComment, Level
from massassi.util import OurMySqlImportBaseCommand


class Command(OurMySqlImportBaseCommand):
    help = 'Imports level comments from mysql database'

    def handle(self, *args, **options):
        cnx = self.get_connection(options)

        cursor = cnx.cursor(dictionary=True)

        query = "SELECT * FROM level_comments ORDER BY comment_id"

        cursor.execute(query)

        for row in cursor.fetchall():
            self.stdout.write("Processing {}".format(row['comment_id']))

            date_created = datetime.fromtimestamp(
                row['comment_time'], tz=pytz.timezone('America/Los_Angeles')
            )

            level = get_level(row['level_id'])
            if not level:
                self.stderr.write("unable to find level {}".format(row['level_id']))
                continue

            user = get_user(row['user_id'])
            if not user:
                self.stderr.write("unable to find user {}".format(row['user_id']))
                continue

            comment = LevelComment(
                id=row['comment_id'],
                level=level,
                user=user,
                comment=strip_tags(row['comment_text']),
                date_created=date_created,
                ip=row['comment_ip'],
            )

            comment.save()

            self.stdout.write("Processed {}".format(row['comment_id']))

        cursor.close()
        cnx.close()


level_cache = {}

def get_level(level_id):
    if level_id not in level_cache:
        try:
            level_cache[level_id] = Level.objects.get(pk=level_id)
        except ObjectDoesNotExist:
            level_cache[level_id] = None

    return level_cache[level_id]


user_cache = {}

def get_user(user_id):
    if user_id not in user_cache:
        try:
            user_cache[user_id] = User.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            user_cache[user_id] = None

    return user_cache[user_id]
