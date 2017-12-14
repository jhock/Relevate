from django.conf.urls import url
from django.contrib.auth import views as django_auth_views
from .examples import examples
from .views import styleguide_views

urlpatterns = []
for example in examples:
  urlpatterns.append(url(r'' + example, styleguide_views.StyleguideView.as_view(), name=example))

urlpatterns.append(url(r'', styleguide_views.StyleguideView.as_view(), name='index'))
