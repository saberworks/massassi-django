from django.db.models import Q
from django.shortcuts import render
from django.views import generic
from django.db import connection

from massassi.dbutil import dictfetchall

from .models import HolidayLogo


class IndexView(generic.View):
    template_name = 'holiday/index.html'

    def get(self, request):
        years = self.fetch_holiday_years()
        return render(request, self.template_name, {'years': years})

    @staticmethod
    def fetch_holiday_years():
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT year AS the_year
                     , COUNT(*) as the_count
                  FROM holiday_logos
              GROUP BY the_year
              ORDER BY the_year
            """)

            return dictfetchall(cursor)


class YearView(generic.View):
    template_name = 'holiday/year.html'

    def get(self, request, year):
        logos = HolidayLogo.objects.filter(year=year).order_by('created_at', 'author')
        return render(request, self.template_name, {'year': year, 'logos': logos})
