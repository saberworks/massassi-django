from django.views import generic

from .models import LevelCategory

#
# CategoryIndexView shows all categories/descriptions/counts and links to the
# category detail page
#
class CategoryIndexView(generic.ListView):
    template_name = 'levels/index.html'
    context_object_name = 'categories'
    paginate_by = 25

    def get_queryset(self):
        return LevelCategory.objects.order_by('name')

#
# CategoryDetailView lists all levels in the specified category ID
#
class CategoryDetailView(generic.DetailView):
    model = LevelCategory
    slug_field = 'path'
    template_name = 'levels/category.html'

#
# LevelView displays detail info about a single level
#
class LevelView(generic.DetailView):
    template_name = 'levels/level.html'
