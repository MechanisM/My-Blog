from django.views.generic.simple import direct_to_template
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.conf import settings
from django.http import HttpResponseRedirect

from tagging.models import TaggedItem
from tagging.utils import get_tag

from node.feeds import LatestEntriesFeed
from node.models import Entry


def main(request):
    nodes = Entry.objects.filter(is_page=False, visible=True).order_by('-created')

    return direct_to_template(request, 'main.html', {
        'nodes': nodes,
    })

def tag_items(request, tag):
    nodes = Entry.objects.order_by('-created')

    tag_instance = get_tag(int(tag))
    if tag_instance is None:
        raise Http404()
    nodes = TaggedItem.objects.get_by_model(nodes, tag_instance)

    return direct_to_template(request, 'main.html', {
        'nodes': nodes,
    })

def item(request, nid_or_slug):
    if nid_or_slug.isdigit():
        node = get_object_or_404(Entry, nid=nid_or_slug)
    else:
        node = get_object_or_404(Entry, slug=nid_or_slug)
        
    return direct_to_template(request, 'item.html', {
        'node': node,
    })

def rss(request):
    FEEDBURNER = getattr(settings, 'FEEDBURNER', None)
    if not FEEDBURNER or request.META['HTTP_USER_AGENT'].startswith('FeedBurner'):
        return LatestEntriesFeed()(request)
    else:
        return HttpResponseRedirect(FEEDBURNER)