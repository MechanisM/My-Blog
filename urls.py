from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

from node.models import sitemaps

urlpatterns = patterns('',
    (r'^$', 'node.views.main'),
    url(r'^node/(\d+)$', 'node.views.item', name='node_view'),
    (r'^taxonomy/term/(\d+)$', 'node.views.tag_items'),
    (r'^rss\.xml$', 'node.views.rss'),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}, name='sitemap'),
    
    (r'^admin/', include(admin.site.urls)),
)


from django.conf import settings

if settings.DEBUG:
    urlpatterns += patterns("django.views",
        url(r"%s(?P<path>.*)$" % settings.MEDIA_URL[1:], "static.serve", {
            "document_root": settings.MEDIA_ROOT,
        })
    )

urlpatterns += patterns('',
    url(r'^(.+)$', 'node.views.item', name='seo_node_view'),
)