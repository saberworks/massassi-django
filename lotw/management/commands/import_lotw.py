from django.utils.timezone import get_current_timezone, make_aware

from massassi.importutil import get_level, get_user
from massassi.util import OurMySqlImportBaseCommand
from lotw.models import LotwHistory, LotwVote

class Command(OurMySqlImportBaseCommand):
    help = 'Imports lotw & votes from mysql database'

    def handle(self, *args, **options):
        self.import_lotw_history(*args, **options)
        self.import_lotw_votes(*args, **options)

    def import_lotw_history(self, *args, **options):
        cnx = self.get_connection(options)
        timezone = get_current_timezone();
        cursor = cnx.cursor(dictionary=True)

        query = "SELECT * FROM lotw_history ORDER BY lotw_time"

        cursor.execute(query)

        for row in cursor.fetchall():
            self.stdout.write("Processing lotw {}...".format(row['lotw_time']), ending='')

            level = get_level(row['level_id'])
            if not level:
                self.stderr.write("unable to find level {}".format(row['level_id']))
                continue

            lotw_time = make_aware(row['lotw_time'], timezone, is_dst=False)
            lotw = LotwHistory(
                level=level,
                lotw_time=row['lotw_time'],
            )

            lotw.save(force_insert=True)

            self.stdout.write("Done")

        cursor.close()
        cnx.close()

    def import_lotw_votes(self, *args, **options):
        cnx = self.get_connection(options)
        timezone = get_current_timezone();
        cursor = cnx.cursor(dictionary=True)

        query = "SELECT * FROM lotw_votes ORDER BY vote_id"

        cursor.execute(query)

        for row in cursor.fetchall():
            self.stdout.write("Processing lotw vote {}".format(row['vote_id']))

            level = get_level(row['level_id'])
            if not level:
                self.stderr.write("unable to find level {}".format(row['level_id']))
                continue

            user = get_user(row['user_id'])
            if not user:
                self.stderr.write("unable to find user {}".format(row['user_id']))
                continue

            ip = row['vote_ip'] if row['vote_ip'] else '0.0.0.0'

            voted_at_with_tz = make_aware(row['vote_time'], timezone, is_dst=False)

            vote = LotwVote(
                id=row['vote_id'],
                user=user,
                level=level,
                voted_at=voted_at_with_tz,
                ip=ip,
            )

            vote.save(force_insert=True)

            self.stdout.write("Done with lotw {}".format(row['vote_id']))

        cursor.close()
        cnx.close()
