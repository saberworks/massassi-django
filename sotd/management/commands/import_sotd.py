import os

from django.core.files import File

from sotd.models import SotD
from massassi.util import OurBaseCommand


class Command(OurBaseCommand):
    help = 'Imports SotD entries from mysql database and local screenshot directory'

    def add_arguments(self, parser):
        super().add_arguments(parser)

        parser.add_argument('--ss_path', nargs='?', type=str, required=True, help='Full path to screenshot directory')

    def handle(self, *args, **options):
        cnx = self.get_connection(options)

        cursor = cnx.cursor(dictionary=True)

        query = "SELECT * FROM sotd ORDER BY sotd_date"

        cursor.execute(query)

        for row in cursor.fetchall():
            date = row['sotd_date'].strftime('%Y-%m-%d')
            ss_file = "{}/{}.jpg".format(options['ss_path'], date)

            if not os.path.isfile(ss_file):
                self.stderr.write("Screenshot for {} missing from filesystem; skipping".format(date))
                continue

            fh = open(ss_file, 'rb')
            django_file = File(fh)

            # original database had some quotes with backslashes ahead of them... grrr
            description = row['description'].replace("\\", "")

            sotd = SotD(
                sotd_date=row['sotd_date'],
                admin_id=row['admin_id'],
                title=row['title'],
                author=row['author'],
                author_email=row['author_email'],
                url=row['url'],
                description=description,
            )

            sotd.image.save("{}.jpg".format(date), django_file, save=True)
            sotd.save()

            self.stdout.write("Processed {}".format(row['sotd_date']))

        cursor.close()
        cnx.close()
