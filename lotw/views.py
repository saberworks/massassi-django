from django.views import generic

from .models import LotwHistory


class IndexView(generic.ListView):
    template_name = 'lotw/index.html'
    context_object_name = 'lotw_list'
    paginate_by = 25

    def get_queryset(self):
        return LotwHistory.objects.order_by('-lotw_time').select_related('level')
