import os
import pytz
import re

from django.utils.datetime_safe import datetime
from django.core.files import File

from levels.models import Level, LevelCategory
from massassi.util import OurMySqlImportBaseCommand


class Command(OurMySqlImportBaseCommand):
    help = 'Imports levels from mysql database, files and screenshots from local directories'

    def add_arguments(self, parser):
        super().add_arguments(parser)

        parser.add_argument('--ss_path', nargs='?', type=str, required=True, help='Full path to screenshot directory')
        parser.add_argument('--files_path', nargs='?', type=str, required=True, help='Path to level files')
        parser.add_argument('--level_id', nargs='?', type=int, required=False, help='Optional level id')
        parser.add_argument('--start_level_id', nargs='?', type=int, required=False, help='Start at this level id')

    def handle(self, *args, **options):
        cnx = self.get_connection(options)

        categories = get_category_hash(cnx)

        cursor = cnx.cursor(dictionary=True)

        query = 'SELECT * FROM levels ORDER BY level_id'
        query_params = ()

        if options['level_id']:
            query = 'SELECT * FROM levels WHERE level_id = %s'
            query_params = (options['level_id'],)

        if options['start_level_id']:
            query = 'SELECT * FROM levels WHERE level_id >= %s'
            query_params = (options['start_level_id'],)

        cursor.execute(query, query_params)

        for row in cursor.fetchall():
            level_id = row['level_id']
            category = categories[row['category_id']]

            self.stdout.write("Processing {} ({})".format(level_id, category))

            screenshot_1 = self.get_screenshot(options['ss_path'], level_id, 1)
            screenshot_2 = self.get_screenshot(options['ss_path'], level_id, 2)

            # filenames appear to be messed up with html entities, try to
            # replace them with the actual characters that are on the
            # filesystem
            file_name = re.sub(r'&#39;', "'", row['file_name'])

            file = self.get_file(options['files_path'], category.path, file_name, level_id)

            if not file:
                continue

            created_at = datetime.fromtimestamp(
                row['timestamp'], tz=pytz.timezone('America/Los_Angeles')
            )

            rating = row['rating'] if row['rating'] >= 0 else 0

            level = Level(
                id=level_id,
                category=category,
                name=row['level_name'],
                description=row['description'],
                author=row['author'],
                email=row['email'],
                created_at=created_at,
                dl_count=row['dl_count'],
                comment_count=row['comment_count'],
                rate_count=row['rate_count'],
                rating=rating,
            )

            level.file.save(file_name, file, save=False)

            if screenshot_1:
                level.screenshot_1.save("{}_{}.jpg".format(level_id, 1), screenshot_1, save=False)

            if screenshot_2:
                level.screenshot_2.save("{}_{}.jpg".format(level_id, 2), screenshot_2, save=False)

            level.save()

        cursor.close()
        cnx.close()

    def get_screenshot(self, ss_path, level_id, ss_number):
        ss_file = "{}/{}_{}.jpg".format(ss_path, level_id, ss_number)

        if not os.path.isfile(ss_file):
            self.stdout.write("Screenshot for {} missing from filesystem; skipping".format(ss_file))
            return None

        fh = open(ss_file, 'rb')
        return File(fh)

    def get_file(self, files_path, category_path, file_name, level_id):
        file = "{}/{}/{}".format(files_path, category_path, file_name)

        if not os.path.isfile(file):
            self.stderr.write("File for level id {} missing from filesystem ({}); skipping".format(level_id, file))
            return None

        fh = open(file, 'rb')
        return File(fh)


def get_category_hash(cnx):
    cursor = cnx.cursor(dictionary=True)

    query = "SELECT * FROM categories ORDER BY category_id"

    cursor.execute(query)

    categories = {}

    for row in cursor.fetchall():
        category = LevelCategory.objects.get(id=row['category_id'])
        categories[row['category_id']] = category

    return categories
