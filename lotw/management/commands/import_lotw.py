from django.core.exceptions import ObjectDoesNotExist

from massassi.util import OurMySqlImportBaseCommand

from levels.models import Level
from lotw.models import LotwHistory, LotwVote
from users.models import User

class Command(OurMySqlImportBaseCommand):
    help = 'Imports lotw & votes from mysql database'

    def handle(self, *args, **options):
        self.import_lotw_history(*args, **options)
        self.import_lotw_votes(*args, **options)

    def import_lotw_history(self, *args, **options):
        cnx = self.get_connection(options)

        cursor = cnx.cursor(dictionary=True)

        query = "SELECT * FROM lotw_history ORDER BY lotw_time"

        cursor.execute(query)

        for row in cursor.fetchall():
            self.stdout.write("Processing lotw {}".format(row['lotw_time']))

            level = get_level(row['level_id'])
            if not level:
                self.stderr.write("unable to find level {}".format(row['level_id']))
                continue

            lotw = LotwHistory(
                level=level,
                lotw_time=row['lotw_time'],
            )

            lotw.save(force_insert=True)

            self.stdout.write("Done with lotw {}".format(row['lotw_time']))

        cursor.close()
        cnx.close()

    def import_lotw_votes(self, *args, **options):
        cnx = self.get_connection(options)

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

            vote = LotwVote(
                id=row['vote_id'],
                user=user,
                level=level,
                voted_at=row['vote_time'],
                ip=ip,
            )

            vote.save(force_insert=True)

            self.stdout.write("Done with lotw {}".format(row['vote_id']))

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
