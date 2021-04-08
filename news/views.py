from django.views import generic

from levels.models import Level
from lotw.models import LotwHistory
from sotd.models import SotD
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
        context['lotw'] = LotwHistory.objects.latest('lotw_time')
        context['sotd'] = SotD.objects.latest('sotd_date')

        return context

# TODO: MonthArchiveView (instead of simple pagination)
class DetailView(generic.View):
    template_name = 'sotd/sotd.html'
