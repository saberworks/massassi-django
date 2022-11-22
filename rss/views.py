import logging

from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Atom1Feed

from news.models import News

logger = logging.getLogger(__name__)

class NewsFeed(Feed):
    title = "The Massassi Temple: News"
    link = "/"
    description = "Latest news from The Massassi Temple"
    feed_type = Atom1Feed
    description_template = "news/feed_item.html"

    def items(self):
        return News.objects.order_by('-date_posted')[:100]

    def item_title(self, item):
        return item.headline

    def item_pubdate(self, item):
        return item.date_posted

    def item_updateddate(self, item):
        return item.date_posted

    def item_author_name(self, obj):
        if(obj):
            return obj.user.username
        else:
            return "UNKNOWN"
