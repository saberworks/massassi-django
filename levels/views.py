import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.db.models import Count, F
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views import generic, View

from massassi.httputil import get_client_ip
from .forms import CommentForm, RatingForm
from .models import Level, LevelCategory, LevelComment, LevelRating

logger = logging.getLogger(__name__)

# Quick access to level object based on level id
def get_level(level_id):
    return Level.objects.get(pk=level_id)

# Quick access to rating row, but check that it exists first
def get_rating(level, user):
    if not user.is_authenticated:
        return None

    try:
        rating = LevelRating.objects.get(level=level, user=user)
    except ObjectDoesNotExist:
        rating = None

    return rating

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

        rating = get_rating(context['level'], self.request.user)

        context['rating_form'] = RatingForm(instance=rating)

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
class CommentView(LoginRequiredMixin, generic.FormView):
    form_class = CommentForm
    template_name = 'levels/comment.html'

    def get(self, request, level_id):
        level = get_level(level_id)

        form = self.form_class()

        return render(request, self.template_name, {'form': form, 'level': level})

    def post(self, request, level_id):
        level = get_level(level_id)

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


class RateView(LoginRequiredMixin, generic.FormView):
    form_class = RatingForm
    template_name = 'levels/rating.html'

    def get(self, request, level_id):
        level = get_level(level_id)
        rating = get_rating(level, request.user)

        form = self.form_class(instance=rating)

        return render(request, self.template_name, {'rating_form': form, 'level': level})

    def post(self, request, level_id):
        level = get_level(level_id)
        rating = get_rating(level, request.user)

        form = self.form_class(request.POST, instance=rating)

        if form.is_valid():
            rating = form.save(commit=False)

            rating.level = level
            rating.user = request.user
            rating.ip = get_client_ip(request)

            rating.save()

            messages.success(request, 'Rating submission successful!')

            return redirect('levels:level', rating.level_id)

        return render(request, self.template_name, {'rating_form': form, 'level': level})

class ReportCommentView(LoginRequiredMixin, View):
    def get(self, request, comment_id):
        comment = LevelComment.objects.get(pk=comment_id)

        context = {
            'user': request.user,
            'comment': comment,
            'level': comment.level,
        }

        body = render_to_string("levels/abuse.txt", context=context)

        send_mail(
            'Comment Abuse Report',
            body,
            'abuse@massassi.net',
            ['massassi.temple@gmail.com'],
            fail_silently=False,
        )

        messages.success(request, 'Abuse report sent.  Staff will review and take action.')

        return redirect('levels:level', comment.level_id)
