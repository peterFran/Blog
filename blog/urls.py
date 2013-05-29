from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^comments/', include('comments.urls')),
    url(r'^articles/', include('articles.urls', namespace='articles'),),
    url(r'^admin/', include(admin.site.urls)),
)
