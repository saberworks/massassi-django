from django.views import generic

from .models import SotD

class IndexView(generic.ListView):
    template_name = 'sotd/index.html'
    context_object_name = 'sotd_list'
    paginate_by = 25

    def get_queryset(self):
        return SotD.objects.order_by('-sotd_date')

class DetailView(generic.DetailView):
    model = SotD
    template_name = 'sotd/sotd.html'
