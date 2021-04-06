from django.views import generic

from .models import News


class IndexView(generic.ListView):
    template_name = 'news/index.html'
    context_object_name = 'news'
    paginate_by = 25

    def get_queryset(self):
        return News.objects.order_by('-date_posted')


class DetailView(generic.View):
    template_name = 'sotd/sotd.html'
