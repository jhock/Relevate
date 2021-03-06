
from django.conf.urls import url

from .views import base_views
from .views import article_views
from .views import link_views
from .views import infographics_view
from .views import post_views
from .views import resources_views
from .views import about_views
from .views import content_creation_views

urlpatterns = [

	url(r'^$', base_views.HomeView.as_view(), name='home'),
  url(r'^(page=(\d+)/)?$', base_views.HomeView.as_view(), name='home'),
	url(r'^new_post/$', article_views.NewPostView.as_view(), name='new_post'),

	# Articles
	# url(r'^articles/$', article_views.ArticleListView.as_view(), name="articles"),
	# This version of article-create takes a junk value slug. For more info see content-creation/article.html
	url(r'^article_create/(?P<slug>[-\w\d\ ]+)/$', article_views.ArticleCreateView.as_view(), name="article_create"),
	# Following line required for 'get' in 'ArticleCreateView'.
	url(r'^article_create/$', article_views.ArticleCreateView.as_view(), name="article_create"),
	url(r'^articles_update/(?P<slug>[-\w\d\ ]+)/$', article_views.ArticleUpdateView.as_view(), name="article_update"),
	url(r'^article/(?P<slug>[-\w\d\ ]+)/$', article_views.ArticleIndividualView.as_view(), name="article_view"),

	url(r'^ck$', content_creation_views.ckeditor_form_view, name='ck'),

	#About
	url(r'^about/$', about_views.AboutView.as_view(), name='about'),
	url(r'^about_create/$', about_views.AboutCreateView.as_view(), name="about_create"),
	url(r'^about_update/(?P<slug>[-\w\d\ ]+)/$', about_views.AboutUpdateView.as_view(), name="about_update"),
	url(r'^about_remove/(?P<pk>\d+)/$', about_views.AboutRemoveView.as_view(), name="about_remove"),

	#Content Creation
	url(r'^content_creation/$', content_creation_views.ContentCreationView.as_view(), name="content_creation"),
	url(r'^content_creation/(?P<slug>[-\w\d\D\ ]+)$', content_creation_views.ContentCreationTagView.as_view(), name="content_creation"),
	url(r'^content_creation_level/(?P<slug>[-\w\d\D\ ]+)$', content_creation_views.ContentCreationLevelView.as_view(), name="content_creation_level"),
	url(r'^content_creation_create/(?P<slug>[-\w\d\ ]+)/$', content_creation_views.ContentCreationCreateView.as_view(), name="content_creation_create"),
	url(r'^content_creation_create/$', content_creation_views.ContentCreationCreateView.as_view(), name="content_creation_create"),
	url(r'^content_creation/(?P<slug>[-\w\d\ ]+)/$', content_creation_views.ContentCreationIndividualView.as_view(), name="content_creation_view"),
	url(r'^content_creation_remove/(?P<pk>\d+)/$', content_creation_views.ContentCreationRemoveView.as_view(), name="content_creation_remove"),
	url(r'^content_creation_update/(?P<slug>[-\w\d\ ]+)/$', content_creation_views.ContentCreationUpdateView.as_view(), name="content_creation_update"),

	# Infographics
	url(r'^infographic/(?P<slug>[-\w\d\ ]+)/$', infographics_view.InfographicView.as_view(), name="infographic_view"),
  #This version of infographic-create takes a junk value slug. For more info see content-creation/infographics.html
	url(r'^article-infographics-create/(?P<slug>[-\w\d\ ]+)$', infographics_view.InfographicCreateView.as_view(),
			name="infographic_create_view"),
	# Following line required for 'get' in 'InfographicCreateView'.
	url(r'^article-infographics-create/$', infographics_view.InfographicCreateView.as_view(),
		name="infographic_create_view"),
	url(r'^article-infographics-update/(?P<slug>[-\w\d\ ]+)/$',
		infographics_view.InfographicUpdateView.as_view(), name="infographic_update_view"),
	
	# Links
	#Following line required for 'get' in 'LinkCreateView'.
	url(r'^link_create/$', link_views.LinkCreateView.as_view(), name="link_create"),
	#This version of link-create takes a junk value slug. For more info see content-creation/link.html
	url(r'^link_create(?P<slug>[-\w\d\ ]+)/$', link_views.LinkCreateView.as_view(), name="link_create"),
	url(r'^link-update/(?P<slug>[-\w\d\ ]+)/$', link_views.LinkUpdateView.as_view(), name="link_update"),
	url(r'^link-preview$', link_views.LinkPreview.as_view(), name='link_preview'),
	url(r'^link/(?P<slug>[-\w\d\ ]+)/$', link_views.LinkIndividualView.as_view(), name="link_view"),

	# Other
	url(r'^all_posts/$', post_views.PostListView.as_view(), name="all_posts"),
	url(r'^post_remove/(?P<pk>\d+)/$', post_views.PostRemoveView.as_view(), name="post_remove"),
	url(r'^post_remove$', post_views.PostRemoveView.as_view(), name="post_remove"),
	url(r'^post_unpublish/(?P<pk>\d+)/$', post_views.PostUnpublishView.as_view(), name="post_unpublish"),
	url(r'^topic_sort/(?P<slug>[-\w\d\&\,\/ ]+)/$', base_views.TopicSortView.as_view(), name="topic_sort"),

	# Search
	url(r'^search_results/$', base_views.SearchView.as_view(), name="search_results"),
	url(r'^advanced_search_results/$', base_views.AdvancedSearchView.as_view(), name="advanced_search_results"),

	# Posts by Tag
	url(r'^posts_by_tag/(?P<tag>\w+)$', post_views.PostsByTag.as_view(), name="posts_by_tag"),

	# Resources
	url(r'^using_relevate/$', resources_views.UsingRelevateView.as_view(), name="using_relevate"),
	url(r'^public_scholarship/$', resources_views.PublicScholarshipView.as_view(), name="public_scholarship"),
	url(r'^report_error/$', resources_views.ReportErrorView.as_view(), name="report_error")
]
