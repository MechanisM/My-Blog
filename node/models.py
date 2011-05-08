import markdown
import datetime
import xmlrpclib

from django.contrib.sites.models import Site
from django.contrib.sitemaps import GenericSitemap
from django.db.models.signals import post_save
from django.db import models

from tagging.fields import TagField
from tagging.models import Tag


class Entry(models.Model):
    nid = models.IntegerField(unique=True, db_index=True, blank=True, null=True)

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, db_index=True)

    body = models.TextField()
    markd = models.TextField(blank=True, null=True)

    coments = models.BooleanField(default=True)

    is_page = models.BooleanField(default=False)
    page_url = models.CharField(max_length=255, blank=True, null=True, db_index=True)

    visible = models.BooleanField(default=True)

    created = models.DateTimeField(default=datetime.datetime.now)
    edited = models.DateTimeField(auto_now=True)

    tags = TagField()

    @models.permalink
    def get_absolute_url(self):
        if self.nid:
            return 'node_view', [str(self.nid)]
        else:
            return 'seo_node_view', [self.slug]

    def get_absolute_disqus_url(self):
        return 'http://%s%s#disqus_thread' % (Site.objects.get_current().domain, self.get_absolute_url())

    def get_absolute_url_with_domain(self):
        return 'http://%s%s' % (Site.objects.get_current().domain, self.get_absolute_url())

    def get_disqus_identifier(self):
        if self.nid:
            return "node/%s" % self.nid
        else:
            return self.slug

    def show_comment(self):
        if not self.is_page and self.coments:
            return True
        return False

    def get_tags(self):
        return Tag.objects.get_for_object(self)

    def get_description(self):
        return self.body.split("<!--break-->")[0]

    def is_next(self):
        body_splited = self.body.split("<!--break-->")
        if len(body_splited)>1 and body_splited[1].strip():
            return True
        return False

    def save(self, *args, **kwargs):
        if self.markd:
            self.body = markdown.markdown(self.markd, ['codehilite', 'video(youtube_width=620, youtube_height=400)'], safe_mode='escape').replace("<p>!break</p>", "<!--break-->")

        super(Entry, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

def ping_handler(sender, instance=None, **kwargs):
    if instance is None:
        return
    rpc = xmlrpclib.Server('http://ping.feedburner.google.com/')
    rpc.weblogUpdates.ping(instance.title, instance.get_absolute_url())

post_save.connect(ping_handler, sender=Entry)

sitemaps = {
    'nodes' : GenericSitemap({
        'queryset': Entry.objects.filter(visible=True),
        'date_field': 'created'},
        changefreq = 'weekly',  priority = 1)
}