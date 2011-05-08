from django.contrib.syndication.views import Feed
from node.models import Entry

class LatestEntriesFeed(Feed):
    title = "TutaMC about Python and Life"
    link = "http://tutamc.com/"
    description = "The best blog about programming and life ;)"

    def items(self):
        return Entry.objects.filter(is_page=False, visible=True).order_by('-created')[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.get_description()