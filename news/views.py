from django.db.models import Q
from django.shortcuts import render
from django.views import generic
from django.db import connection

from massassi.dbutil import dictfetchall

from levels.models import Level
from lotw.models import LotwHistory
from sotd.models import SotD
from .forms import NewsSearchForm
from .models import News


class IndexView(generic.ListView):
    template_name = 'news/index.html'
    context_object_name = 'news'
    paginate_by = 25

    def get_queryset(self):
        return News.objects \
                   .select_related('user') \
                   .extra(select={'news_date': 'DATE(date_posted)'}) \
                   .order_by('-date_posted')

    # Look up things like recent levels list, sotd, lotw
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['recent_levels'] = Level.objects.order_by('-created_at')[:6]
        context['lotw'] = LotwHistory.objects.select_related('level').latest('lotw_time')
        context['sotd'] = SotD.objects.latest('sotd_date')

        return context

class OldNewsView(generic.View):
    template_name = 'news/old.html'

    def get(self, request):
        form = NewsSearchForm()
        years = self.fetch_news_years()
        return render(request, self.template_name, {'years': years, 'form': form})

    @staticmethod
    def fetch_news_years():
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT CAST(EXTRACT(YEAR FROM date_posted) AS INTEGER) AS the_year
                     , COUNT(*) as the_count
                  FROM news
              GROUP BY the_year
              ORDER BY the_year
            """)

            return dictfetchall(cursor)

class YearView(generic.View):
    template_name = 'news/year.html'

    def get(self, request, year):
        months = self.fetch_news_months(year)
        return render(request, self.template_name, {'year': year, 'months': months})

    @staticmethod
    def fetch_news_months(year):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT CAST(EXTRACT(MONTH FROM date_posted) AS INTEGER) AS the_month
                     , COUNT(*) as the_count
                  FROM news
                  WHERE DATE_PART('year', date_posted) = %s
              GROUP BY the_month
              ORDER BY the_month
            """, [year])

            return dictfetchall(cursor)

class MonthView(generic.ListView):
    template_name = 'news/month.html'
    context_object_name = 'news'

    def get_queryset(self):
        return News.objects\
            .filter(
                date_posted__year=self.kwargs['year'],
                date_posted__month=self.kwargs['month']
            ) \
            .select_related('user') \
            .extra(select={'news_date': 'DATE(date_posted)'}) \
            .order_by('date_posted')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['year'] = self.kwargs['year']
        context['month'] = self.kwargs['month']

        return context

class SearchView(generic.View):
    template_name = 'news/search.html'

    def get(self, request):
        form = NewsSearchForm()
        results = []
        terms = None

        # form was submitted???
        if 'terms' in request.GET:
            form = NewsSearchForm(request.GET)

            if form.is_valid():
                terms = form.cleaned_data['terms']

                results = News.objects\
                    .filter(Q(story__search=terms) | Q(headline__search=terms)) \
                    .select_related('user') \
                    .extra(select={'news_date': 'DATE(date_posted)'}) \
                    .order_by('-date_posted')

        return render(request, self.template_name, {'form': form, 'news': results, 'terms': terms})
