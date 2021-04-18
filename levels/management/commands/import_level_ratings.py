from levels.models import LevelRating
from massassi.importutil import get_level, get_user
from massassi.util import OurMySqlImportBaseCommand


class Command(OurMySqlImportBaseCommand):
    help = 'Imports level ratings from mysql database'

    def handle(self, *args, **options):
        cnx = self.get_connection(options)

        cursor = cnx.cursor(dictionary=True)

        query = "SELECT * FROM level_ratings ORDER BY rating_id"

        cursor.execute(query)

        for row in cursor.fetchall():
            self.stdout.write("Processing level_rating {}...".format(row['rating_id']), ending='')

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

            self.stdout.write("Done")

        cursor.close()
        cnx.close()
