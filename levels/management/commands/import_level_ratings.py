from django.core.exceptions import ObjectDoesNotExist

from users.models import User
from levels.models import LevelRating, Level
from massassi.util import OurMySqlImportBaseCommand


class Command(OurMySqlImportBaseCommand):
    help = 'Imports level ratings from mysql database'

    def handle(self, *args, **options):
        cnx = self.get_connection(options)

        cursor = cnx.cursor(dictionary=True)

        query = "SELECT * FROM level_ratings ORDER BY rating_id"

        cursor.execute(query)

        for row in cursor.fetchall():
            self.stdout.write("Processing rating {}".format(row['rating_id']))

            level = get_level(row['level_id'])
            if not level:
                self.stderr.write("unable to find level {}".format(row['level_id']))
                continue

            user = get_user(row['user_id'])
            if not user:
                self.stderr.write("unable to find user {}".format(row['user_id']))
                continue

            rating = LevelRating(
                id=row['rating_id'],
                level=level,
                user=user,
                ip=row['user_ip'],
                rating=row['rating_score'],
                created_by=user,
                last_modified_by=user,
            )

            rating.save(force_insert=True)

            self.stdout.write("Done with rating {}".format(row['rating_id']))

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
