from django.contrib import admin
from articles.models import Blog, Entry, Revision, Comment

admin.site.register(Blog)
admin.site.register(Entry)
admin.site.register(Revision)
admin.site.register(Comment)