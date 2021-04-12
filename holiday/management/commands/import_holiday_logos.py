import os
import re
from os.path import isfile, join
from pprint import pprint

from django.core.files import File

from holiday.models import HolidayLogo
from massassi.util import OurMySqlImportBaseCommand


class Command(OurMySqlImportBaseCommand):
    help = 'Imports holiday logos from mysql database and local directories'

    def add_arguments(self, parser):
        super().add_arguments(parser)

        """
        Note: massassi has two systems for managing holiday logo contest
        entries.  The first one uses a combination of mysql tables to
        store metadata and then filesystem to store the actual images.
        
        The second system stores everything on the filesystem.  Years
        each have their own directory and usernames are included in the
        image file name.
        """

        parser.add_argument('--older_files_path', nargs='?', type=str, required=True, help='Path to older logo files')
        parser.add_argument('--newer_files_path', nargs='?', type=str, required=True, help='Path to newer logo files')

    def handle(self, *args, **options):
        self.import_older_logos(*args, **options)
        self.import_newer_logos(*args, **options)

    def import_older_logos(self, *args, **options):
        cnx = self.get_connection(options)

        cursor = cnx.cursor(dictionary=True)

        query = """
            SELECT * FROM hlclogos l
              JOIN hlcauthors a ON l.authorid = a.id
          ORDER BY l.id;

        """

        cursor.execute(query)

        for row in cursor.fetchall():
            author = row['name']
            year = row['year']
            filename = row['filename']

            self.stdout.write("Processing {} ({})".format(author, year))

            logo = self.get_older_logo(options['older_files_path'], year, filename)

            if not logo:
                self.stderr.write("ERROR! {} {}".format(year, filename))
                continue

            holiday_logo = HolidayLogo(
                author=author,
                year=year,
                is_enabled=row['enabled'],
                is_in_rotation=row['rotation'],
                created_at=row['date'],
            )

            holiday_logo.logo.save(filename, logo)

        cursor.close()
        cnx.close()

    # Expect files to be in directory, but if not, check <year>/<file>
    def get_older_logo(self, path, year, filename):
        file = "{}/{}".format(path, filename)

        if not os.path.isfile(file):
            self.stderr.write("Logo for {} {} missing from filesystem...".format(file, year))
            file = "{}/{}/{}".format(path, year, filename)

            if not os.path.isfile(file):
                self.stderr.write("Also checked {} but still not found, skipping".format(file))
                return None

        fh = open(file, 'rb')
        return File(fh)

    def import_newer_logos(self, *args, **options):
        self.stdout.write("checking {}".format(options['newer_files_path']))

        year_pattern = re.compile(r'(\d\d\d\d)$')
        author_pattern = re.compile(r'^([^-]+)-*\.')

        for dirpath, dirnames, files in os.walk(options['newer_files_path']):
            self.stdout.write(f'Found directory: {dirpath}')

            # split year from dir name
            pprint(dirpath)
            year_result = re.search(year_pattern, dirpath)

            if not year_result:
                continue

            year = year_result.group(1)

            # text_after = re.sub(regex_search_term, regex_replacement, text_before)

            for file_name in files:
                self.stdout.write("Processing: {}".format(file_name))

                author = re.sub(r'\.\w*$', '', file_name)
                author = re.sub(r'-+$', '', author)

                self.stdout.write("Processing {} ({})".format(author, year))

                logo = self.get_newer_logo(dirpath, file_name)

                if not logo:
                    self.stderr.write("ERROR! {} {}".format(year, file_name))
                    continue

                holiday_logo = HolidayLogo(
                    author=author,
                    year=year,
                    is_enabled=True,
                    is_in_rotation=True,
                )

                holiday_logo.logo.save(file_name, logo)

    # Expect files to be in directory, but if not, check <year>/<file>
    def get_newer_logo(self, dirpath, file_name):
        file = "{}/{}".format(dirpath, file_name)
        if not os.path.isfile(file):
            self.stderr.write("Logo for {} missing from filesystem...".format(file))
            return

        fh = open(file, 'rb')
        return File(fh)
