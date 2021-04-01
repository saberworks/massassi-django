import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, F
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import generic

from massassi.httputil import get_client_ip

from .forms import CommentForm
from .models import Level, LevelCategory, LevelComment

logger = logging.getLogger(__name__)


#
# CategoryIndexView shows all categories/descriptions/counts and links to the
# category detail page
#
class CategoryIndexView(generic.ListView):
    template_name = 'levels/index.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return LevelCategory.objects \
            .order_by('name') \
            .annotate(level_count=Count('level'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['games'] = {
            "jk": "Jedi Knight",
            "mots": "Mysteries of the Sith",
            "jo": "Jedi Outcast",
            "ja": "Jedi Academy",
            "other": "Other",
        }

        return context

#
# CategoryDetailView lists all levels in the specified category ID
#
class CategoryDetailView(generic.ListView):
    model = Level
    template_name = 'levels/category.html'
    context_object_name = 'levels'
    paginate_by = 25
    _category = None

    def get_queryset(self):
        path = self.kwargs['path']

        # Save the category for later so it can be added to context; this
        # avoids a second db query
        self._category = LevelCategory.objects.get(path=path)

        return Level.objects \
            .filter(category=self._category) \
            .order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['category'] = self._category

        return context

#
# LevelView displays detail info about a single level
#
class LevelDetailView(generic.DetailView):
    model = Level
    template_name = 'levels/level.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['comments'] = LevelComment.objects \
            .filter(level=context['level']).select_related('user')

        return context

#
# LevelDownloadView is the actual download operation (simple page with meta
# redirect to the download, allows us to count downloads)
#
class LevelDownloadView(generic.DetailView):
    template_name = 'levels/download.html'
    model = Level

    # This is a BS implementation to increment the counter; doesn't seem
    # like django provides a generic place to actually put code in these
    # generic views?
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        level = self.object

        level.dl_count = F('dl_count') + 1
        level.save()

        return context


#
# CommentView is the add comment form & handler
#
@method_decorator(login_required, name='dispatch')
class CommentView(generic.FormView):
    form_class = CommentForm
    template_name = 'levels/comment.html'

    def get_level(self, level_id):
        return Level.objects.get(pk=level_id)

    def get(self, request, level_id):
        level = self.get_level(level_id)

        form = self.form_class()

        return render(request, self.template_name, {'form': form, 'level': level})

    def post(self, request, level_id):
        level = self.get_level(level_id)

        form = self.form_class(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)

            comment.level = level
            comment.user = request.user
            comment.ip = get_client_ip(request)

            comment.save()

            messages.success(request, 'Comment submission successful!')

            return redirect('levels:level', comment.level_id)

        return render(request, self.template_name, {'form': form})


class RateView(generic.FormView):
    pass

class ReportCommentView(generic.FormView):
    pass
