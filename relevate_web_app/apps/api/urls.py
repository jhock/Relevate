from django.conf.urls import url, include
from .views.feed_view import FeedView

urlpatterns = [
	url(r'^post-feeds/$', FeedView.as_view()),
	url(r'^post-feeds/(?P<feed_index>[0-9]+)/$', FeedView.as_view()),

]