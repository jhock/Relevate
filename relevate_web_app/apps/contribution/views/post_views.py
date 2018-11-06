from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import View
from ...profiles.models.user_models import UserProfile
from ...profiles.models.contributor_model import ContributorProfile
from ..models.post_model import Post
from ..models.article_model import Article
from ..models.infographic_model import Infographic
from ..models.link_model import Link
from ..models.topic_model import Topics
import json
from braces.views import LoginRequiredMixin
from django.views.generic import DeleteView
from django.core.exceptions import PermissionDenied
from itertools import chain


class PostListView(LoginRequiredMixin, View):

    def get(self, request):
        '''
        Lists all posts for a contributor. If the accessing user is not a
        contributor then they get sent home.
        '''
        user_prof = UserProfile.objects.get(user=request.user)
        if (not user_prof.is_contributor):
            return HttpResponseRedirect('contribution:home')
        #returns view for master relevate account (may be changed to staff at some point)
        if (user_prof.user.email == "relevate@outlook.com"):
            contrib_prof = ContributorProfile.objects.get(user_profile=user_prof)
            #allows all post to be seen, not just the user's.
            posts = Post.objects.all()
            pending_posts = posts.filter(is_pending_adviser=True)
            published_posts = posts.filter(isPublished=True)
            saved_posts = posts.filter(is_pending_adviser=False, isPublished=False)
            deleted_posts = posts.filter(is_deleted=True)
            return render(request, 'all_posts.html',
                          {
                              'user_prof': user_prof,
                              'contrib_prof': contrib_prof,
                              #superuser_override allows the superuser (now relevate@outlook.com) to edit and deleted posts that they did not create.
                              'superuser_override': True,
                              'posts': posts,
                              'pending_posts': pending_posts,
                              'published_posts': published_posts,
                              'saved_posts': saved_posts,
                              'has_adviser': contrib_prof.has_adviser,
                              'deleted_posts': posts.filter(is_deleted=True)
                          })
        else:
            contrib_prof = ContributorProfile.objects.get(user_profile = user_prof)
            posts = Post.objects.filter(contributor=contrib_prof, is_deleted=False).order_by('-createdDate')
            pending_posts = posts.filter(is_pending_adviser = True)
            published_posts = posts.filter(isPublished = True)
            saved_posts = posts.filter(is_pending_adviser = False, isPublished = False)
            deleted_posts = posts.filter(is_deleted = True)
            return render(request, 'all_posts.html',
                {
                    'user_prof': user_prof,
                    'contrib_prof': contrib_prof,
                    'posts': posts,
                    'pending_posts': pending_posts,
                    'published_posts': published_posts,
                    'saved_posts': saved_posts,
                    'has_adviser': contrib_prof.has_adviser,
                    'deleted_posts': deleted_posts
                })

class PermissionMixin(object):

    def get_object(self, *args, **kwargs):
        obj = super(PermissionMixin, self).get_object(*args, **kwargs)
        if self.request.user.email == 'relevate@outlook.com':
            return obj
        if not obj.contributor.user_profile.user == self.request.user:
            raise PermissionDenied()
        else:
            return obj

class PostRemoveView(PermissionMixin, DeleteView):
    #
    # def post(self, request):
    # 	'''
    # 	Sets the `is_deleted` value of the post object to true so it
    # 	behaves as a deleted post.
    #
    # 	:param slug: The unique slug of the post.
    # 	'''
    # 	response = {}
    # 	try:
    # 		post = Post.objects.get(slug=str(request.POST.get('slug')))
    # 		post.is_deleted = True
    # 		post.save()
    # 		response["deleted"] = True
    # 	except (AttributeError, ValueError, KeyError):
    # 		response["deleted"] = False
    # 	return HttpResponse(json.dumps(response))

    model = Post
    success_url = reverse_lazy('contribution:all_posts')

class PostUnpublishView(View):
    def post(self, request):

        response = {}
        try:
            post = Post.objects.get(slug=str(request.POST.get('slug')))
            post.isPublished = False
            post.save()
            response["Published"] = False
        except (AttributeError, ValueError, KeyError):
            response["Published"] = True
        return HttpResponse(json.dumps(response))

class PostsByTag(View):
    """View handing selecting posts for a selected tag. Directs to home page currently, will eventually
    direct to topic_sort.html. 'tag' value provides the name of the selected tag."""
    def get(self, request, tag):

        topic = Topics.objects.get(name=tag)
        tagged_articles = Post.objects.filter(article__article_topics=topic)
        tagged_links = Post.objects.filter(link__topics=topic)
        tagged_infographics = Post.objects.filter(infographic__topics=topic)
        all_tagged = list(chain(tagged_articles, tagged_infographics, tagged_links))
        return render(request, 'home.html', {'published_posts': all_tagged})












