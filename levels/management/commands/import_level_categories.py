from levels.models import LevelCategory
from massassi.util import OurMySqlImportBaseCommand


class Command(OurMySqlImportBaseCommand):
    help = 'Imports level categories from mysql database'

    def handle(self, *args, **options):
        cnx = self.get_connection(options)

        cursor = cnx.cursor(dictionary=True)

        query = "SELECT * FROM categories ORDER BY category_id"

        cursor.execute(query)

        for row in cursor.fetchall():
            game = _get_game(row['category_path'])

            path = row['category_path']

            if path == 'jkmods':
                path = 'jkmod'

            if path == 'motsmods':
                path = 'motsmod'

            cat = LevelCategory(
                id=row['category_id'],
                name=row['category_name'],
                path=path,
                enable_3dpreview=row['3dpreview'],
                game=game,
            )

            cat.save(force_insert=True)

            self.stdout.write("Processed {}".format(row['category_name']))

        cursor.close()
        cnx.close()

def _get_game(path):
    if path.startswith('jk'): return 'jk'
    if path.startswith('mots'): return 'mots'
    if path.startswith('jo'): return 'jo'
    if path.startswith('ja'): return 'ja'
    if path.startswith('mad'): return 'other'

    return 'unknown'
