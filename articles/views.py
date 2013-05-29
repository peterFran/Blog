from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from articles.models import Comment, CurrentVersion, Entry, Revision, Blog
from django.views.generic import DetailView, ListView
from django.http import Http404
from django.contrib.auth.models import User
# from articles.models import Node, Article, Comment, Edit
# # ...
class GeneralListView(ListView):
    def get_context_data(self, **kwargs):
        context = super(GeneralListView, self).get_context_data(**kwargs)
        context['title'] = "Peter's Blogosphere"
        context['page_title'] = "Blogs"
        return context
class GeneralDetailView(DetailView):
    def get_context_data(self, **kwargs):
        context = super(GeneralDetailView, self).get_context_data(**kwargs)
        context['title'] = "Peter's Blogosphere"
        context['page_title'] = "Blog"
        return context

class EntryDetailView(GeneralDetailView):
    context_object_name = "article"
    model = Revision
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(EntryDetailView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['page_title'] = self.object.entry.title
        context['related_entries'] = entries = Entry.objects.filter(blog=self.object.entry.blog)
        context['comments'] = Comment.objects.filter(entry=self.object.entry)
        return context
    def get_object(self):
        entry = get_object_or_404(Entry, pk=self.kwargs["entry_id"])
        cur = get_object_or_404(CurrentVersion, entry=entry)
        return cur.current_version

class EntryListView(GeneralListView):
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(EntryListView, self).get_context_data(**kwargs)
        # Set page title
        context['page_title'] = Blog.objects.get(id=self.kwargs["blog_id"])
        return context

    def get_queryset(self):
        return CurrentVersion.objects.filter(entry__blog=self.kwargs["blog_id"]).order_by('-entry__original_pub_date')

class AuthorListView(GeneralListView):
    def get_context_data(self, **kwargs):
        # call super
        context = super(AuthorListView, self).get_context_data(**kwargs)
        context['page_title'] = "Authors"
        
        return context
class AuthorDetailView(GeneralDetailView):
    def get_context_data(self, **kwargs):
        # call super
        context = super(AuthorDetailView, self).get_context_data(**kwargs)
        context['page_title'] = self.object.first_name+" "+self.object.last_name
        context['related_blogs'] = Blog.objects.filter(author=self.object)
        return context
    def get_object(self):
        obj = super(AuthorDetailView, self).get_object()
        if len(Blog.objects.filter(author=self.kwargs['pk']))==0:
            raise Http404
        return obj

class CommentListView(GeneralListView):
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CommentListView, self).get_context_data(**kwargs)
        # Get user
        context['user_object'] = User.objects.get(id=self.kwargs["user_id"])
        # Set page title
        context['page_title'] = unicode(context['user_object'])
        return context

    def get_queryset(self):
        return Comment.objects.filter(author=self.kwargs["user_id"]).order_by('-added')





    # try:
    #     selected_choice = p.choice_set.get(pk=request.POST['choice'])
    # except (KeyError, Choice.DoesNotExist):


    #     # Redisplay the poll voting form.
    #     return render_to_response('polls/detail.html', {
    #         'poll': p,
    #         'error_message': "You didn't select a choice.",
    #     }, context_instance=RequestContext(request))
    # else:
    #     selected_choice.votes += 1
    #     selected_choice.save()
    #     # Always return an HttpResponseRedirect after successfully dealing
    #     # with POST data. This prevents data from being posted twice if a
    #     # user hits the Back button.
    #     return HttpResponseRedirect(reverse('polls.views.results', args=(p.id,)))# Create your views here.
# 	# def getComments(node_id):

def comment(request):
    comment = Comment(
        entry=Entry.objects.get(pk=request.POST['entry_id']),
        author=User.objects.get(pk=request.POST['author']),
        comment=request.POST['comment'],
    )
    # if this is a reply to a comment, not to a post
    if request.POST['parent_id'] != '':
        comment.parent = Comment.objects.get(pk=request.POST['parent_id'])
    comment.save()
    return HttpResponseRedirect(reverse('articles:article', args=(comment.entry.id,)))
