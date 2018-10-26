from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.urls import reverse
from ...profiles.models.user_models import UserProfile
from ...profiles.models.contributor_model import ContributorProfile
from braces.views import LoginRequiredMixin
from ..models.post_model import Post
from ..forms.search_forms import SearchForm
from ..modules.search_util import get_query
from ..models.post_model import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy
from itertools import chain


class HomeView(View):

    '''
    Relevate Home View
    '''

    def get(self, request):
        """
        Returns the home page.
        """
        posts = Post.objects.all().order_by('-publishedDate')
        published = posts.filter(isPublished=True)

        page = request.GET.get('page', 1)
        paginator = Paginator(published, 8)
        try:
            published_posts = paginator.page(page)
        except PageNotAnInteger:
            published_posts = paginator.page(1)
        except EmptyPage:
            published_posts = paginator.page(paginator.num_pages)

        search_form = SearchForm()
        if request.user.is_authenticated:
            user_prof = UserProfile.objects.get(user=request.user)
            already_sel = user_prof.topics_preferences.all().order_by('-name')
            preference_posts = posts.filter(article__article_topics__in=already_sel).distinct() | posts.filter(
                link__topics__in=already_sel).distinct() | posts.filter(infographic__topics__in=already_sel).distinct()
            published_posts = Post.objects.exclude(id__in=preference_posts)
            if (user_prof.is_contributor):
                contrib_prof = ContributorProfile.objects.get(user_profile=user_prof)
                already_sel = contrib_prof.expertise_topics.all().order_by('-name')
                preference_posts = posts.filter(article__article_topics__in=already_sel).distinct() | posts.filter(link__topics__in=already_sel).distinct() | posts.filter(infographic__topics__in=already_sel).distinct()
                published_posts = Post.objects.exclude(id__in=preference_posts)
                #    topics = contrib_prof.expertise_topics.all()
             #    already_sel = []
             #    count = 0
             #    for t in topics:
             #        already_sel.append(t)
             #        print t
             #        count=count+1
             #    count=len(already_sel)
             #    for r in already_sel:
             #        print r
                return render(request, "home.html", {'preference_posts': preference_posts, 'already_sel': already_sel, 'user_prof': user_prof, 'contrib_prof': contrib_prof, 'published_posts': published_posts, "search_form": search_form})
            else:
                return render(request, "home.html", {'preference_posts': preference_posts, 'already_sel': already_sel, 'user_prof': user_prof, 'published_posts': published_posts, "search_form": search_form})
        else:
            return render(request, "home.html", {'published_posts': published_posts, "search_form": search_form})


class TopicSortView(View):

    '''
    Relevate View for a selected topic (shows only posts with that topic tagged)
    '''

    def get(self, request, slug):
        """
        Returns the topic sort page.
        """
        posts = Post.objects.all()
        published_article_posts = posts.filter(is_article=True, isPublished=True)
        published_article_posts = published_article_posts.filter(article__article_topics__name=slug)
        published_link_posts = posts.filter(is_link=True, isPublished=True)
        published_link_posts = published_link_posts.filter(link__topics__name=slug)
        published_infographic_posts = posts.filter(is_infographic=True, isPublished=True)
        published_infographic_posts = published_infographic_posts.filter(infographic__topics__name=slug)
        count = published_article_posts.count() + published_infographic_posts.count() + published_link_posts.count()
        if request.user.is_authenticated:
            user_prof = UserProfile.objects.get(user=request.user)
            if (user_prof.is_contributor):
                contrib_prof = ContributorProfile.objects.get(user_profile=user_prof)
                return render(request, "topic_sort.html", {'user_prof': user_prof, 'contrib_prof': contrib_prof, 'published_article_posts': published_article_posts, 'published_link_posts': published_link_posts, 'published_infographic_posts': published_infographic_posts, 'count': count})
            else:
                return render(request, "topic_sort.html", {'user_prof': user_prof, 'published_article_posts': published_article_posts, 'published_link_posts': published_link_posts, 'published_infographic_posts': published_infographic_posts, 'count': count})
        else:
            return render(request, "topic_sort.html", {'published_article_posts': published_article_posts, 'published_link_posts': published_link_posts, 'published_infographic_posts': published_infographic_posts, 'count': count})

class SearchView(View):
    """
    Display a Blog List page filtered by the search query.
    """
    def get(self, request):

        search_query = request.GET.get('searchbox', None)
        # searches using the search util for post title, topics, contributor first and last name.
        article_title_result = get_query(search_query, ['article__title', 'article__article_topics__name', 'contributor__user_profile__user__first_name', 'contributor__user_profile__user__last_name'])
        link_title_result = get_query(search_query, ['link__title', 'link__topics__name', 'contributor__user_profile__user__first_name', 'contributor__user_profile__user__last_name'])
        infographic_title_result = get_query(search_query, ['infographic__title', 'infographic__topics__name', 'contributor__user_profile__user__first_name', 'contributor__user_profile__user__last_name'])
        posts = Post.objects.all()
        published_article_posts = posts.filter(is_article=True, isPublished=True)
        published_article_posts = published_article_posts.filter(article_title_result).distinct()
        published_link_posts = posts.filter(is_link=True, isPublished=True)
        published_link_posts = published_link_posts.filter(link_title_result).distinct()
        published_infographic_posts = posts.filter(is_infographic=True, isPublished=True)
        published_infographic_posts = published_infographic_posts.filter(infographic_title_result).distinct()
        count = published_article_posts.count() + published_infographic_posts.count() + published_link_posts.count()
        if request.user.is_authenticated:
            user_prof = UserProfile.objects.get(user=request.user)
            if user_prof.is_contributor:
                contrib_prof = ContributorProfile.objects.get(user_profile=user_prof)
                return render(request, "search_results.html",  {'user_prof': user_prof, 'contrib_prof': contrib_prof, 'published_article_posts': published_article_posts, 'published_link_posts': published_link_posts, 'published_infographic_posts': published_infographic_posts, 'count': count})
            else:
                return render(request, "search_results.html",  {'user_prof': user_prof, 'published_article_posts': published_article_posts, 'published_link_posts': published_link_posts, 'published_infographic_posts': published_infographic_posts, 'count': count})
        else:
            return render(request, "search_results.html", {'published_article_posts': published_article_posts,
                                                       'published_link_posts': published_link_posts,
                                                       'published_infographic_posts': published_infographic_posts,
                                                       'count': count})
















