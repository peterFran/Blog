from django.conf.urls import patterns, include, url
from articles.models import Blog, Entry, Revision, CurrentVersion
from django.contrib.auth.models import User
import articles.views as views
urlpatterns = patterns('articles.views',
    url(r'^$',
        views.GeneralListView.as_view(
            queryset=Blog.objects.all().order_by('-date_created')[:10],
            context_object_name='latest_blog_list',
            template_name='articles/index.html')),
    url(r'^(?P<blog_id>\d+)/blog/$',
        views.EntryListView.as_view(
            context_object_name='latest_article_list',
            template_name='articles/blog.html')),
    url(r'^(?P<entry_id>\d+)/entry/$',
        views.EntryDetailView.as_view(
            model=Revision,
            template_name="articles/article.html"), 
        name='article'),
    url(r'^authors/$',
        views.AuthorListView.as_view(
            context_object_name='author_list',
            queryset=User.objects.filter(id__in=Blog.objects.all().values_list("author_id",flat=True)).distinct(),
            template_name="articles/users.html"),
        name='authorlist'),
    url(r'^(?P<pk>\d+)/author/$',
        views.AuthorDetailView.as_view(
            model=User,
            template_name="articles/author.html"), 
        name='author'),
    url(r'^(?P<user_id>\d+)/comments/$',
        views.CommentListView.as_view(
            context_object_name='comment_list',
            template_name="articles/commentlist.html"), 
        name='comments'),
    url(r'^comment/$',
        views.comment,
        name="comment"),
    url(r'^newentry/$',
        views.createEntry,
        name="entry"),
)
