from django.contrib import admin
from node.models import Entry


class EntryAdmin(admin.ModelAdmin):
    list_display = ('nid', 'title', 'is_page', 'page_url', 'created', 'edited')
    list_filter = ('is_page', 'created', 'edited', )
    prepopulated_fields = {"slug": ("title",)}
admin.site.register(Entry, EntryAdmin)