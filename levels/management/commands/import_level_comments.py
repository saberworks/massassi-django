import pytz

from django.utils.datetime_safe import datetime
from django.utils.html import strip_tags

from levels.models import LevelComment
from massassi.importutil import get_level, get_user
from massassi.util import OurMySqlImportBaseCommand


class Command(OurMySqlImportBaseCommand):
    help = 'Imports level comments from mysql database'

    def handle(self, *args, **options):
        cnx = self.get_connection(options)

        cursor = cnx.cursor(dictionary=True)

        query = "SELECT * FROM level_comments ORDER BY comment_id"

        cursor.execute(query)

        for row in cursor.fetchall():
            self.stdout.write("Processing level_comment {}...".format(row['comment_id']), ending='')

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
                created_by=user,
                last_modified_by=user,
            )

            comment.save(force_insert=True)

            self.stdout.write("Done")

        cursor.close()
        cnx.close()
