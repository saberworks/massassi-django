from abc import ABC

from django.core.management import BaseCommand
from mysql.connector import connection


class OurBaseCommand(BaseCommand, ABC):

    def add_arguments(self, parser):
        parser.add_argument('--mysql_host', nargs='?', type=str, required=True)
        parser.add_argument('--mysql_user', nargs='?', type=str, required=True)
        parser.add_argument('--mysql_pass', nargs='?', type=str, required=True)
        parser.add_argument('--mysql_db',   nargs='?', type=str, required=True)

    @staticmethod
    def get_connection(options):
        cnx = connection.MySQLConnection(
            host=options['mysql_host'],
            user=options['mysql_user'],
            password=options['mysql_pass'],
            database=options['mysql_db'],
        )

        return cnx
