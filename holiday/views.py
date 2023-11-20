import datetime
import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views import generic
from django.db import connection
from django.http import HttpResponse

from massassi.dbutil import dictfetchall

from .models import HolidayLogo
from .forms import EnterForm

logger = logging.getLogger(__name__)


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
                 WHERE is_in_rotation=True
              GROUP BY the_year
              ORDER BY the_year DESC
            """)

            return dictfetchall(cursor)


class RandomUrlView(generic.View):
    def get(self, request):
        random_logo = HolidayLogo.objects.random()
        random_logo_url = settings.SITE_URL + random_logo.logo.url
        return redirect(random_logo_url)

class YearView(generic.View):
    template_name = 'holiday/year.html'

    def get(self, request, year):
        logos = HolidayLogo.objects.filter(year=year).filter(is_in_rotation=True).order_by('created_at', 'author')
        return render(request, self.template_name, {'year': year, 'logos': logos})

class EnterView(LoginRequiredMixin, generic.FormView):
    form_class = EnterForm
    template_name = 'holiday/enter.html'

    def get(self, request):
        form = self.form_class()

        year = datetime.date.today().year

        return render(request, self.template_name, {'form': form, 'year': year})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        year = datetime.date.today().year

        if form.is_valid():
            logo = form.save(commit=False)

            logo.user = request.user
            logo.year = year
            logo.is_in_rotation = False

            logo.save()

            messages.success(request, 'Logo has been submitted, thank you!  It will show up in the list after it is approved.')

            return redirect('holiday:year', year)

        return render(request, self.template_name, {'form': form})
