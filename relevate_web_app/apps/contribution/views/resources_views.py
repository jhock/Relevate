from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.urls import reverse
from ...profiles.models.user_models import UserProfile
from ...profiles.models.contributor_model import ContributorProfile
from ..forms.content_creation_form import ContentCreateForm
from ..models.content_creation_model import ContentCreation
from braces.views import LoginRequiredMixin
from ..models.post_model import Post
from ..forms.search_forms import SearchForm
from ..modules.search_util import get_query
from ..models.post_model import Post
from django.urls import reverse_lazy
from itertools import chain


class PublicScholarshipView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            user_prof = UserProfile.objects.get(user=user)
            if user_prof.is_contributor:
                contrib_prof = ContributorProfile.objects.get(user_profile=user_prof)
                can_edit = False
                posts = ContentCreation.objects.all()
                posts = posts.filter(public_scholarship_or_content_creation=True)
                # checks the group "Content Creation Contributor" for the user. If this group has not yet been created, create
                # and assign users in the admin page.
                if user.groups.filter(name='Content Creation Contributor').exists():
                    can_edit = True
                return render(request, "public_scholarship.html",
                              {'user_prof': user_prof, 'contrib_prof': contrib_prof, 'can_edit': can_edit, 'posts': posts})
            else:
                return render(request, "home.html", {'user_prof': user_prof})
        else:
            return render(request, "home.html")


class UsingRelevateView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user_prof = UserProfile.objects.get(user=request.user)
            if user_prof.is_contributor:
                contrib_prof = ContributorProfile.objects.get(user_profile=user_prof)
                return render(request, "using_relevate.html", {'user_prof': user_prof, 'contrib_prof': contrib_prof})
            else:
                return render(request, "home.html", {'user_prof': user_prof})
        else:
            return render(request, "home.html")

class ReportErrorView(View):
    def get(selfself,request):
        if request.user.is_authenticated:
            user_prof = UserProfile.objects.get(user=request.user)
            if user_prof.is_contributor:
                contrib_prof = ContributorProfile.objects.get(user_profile=user_prof)
                return render(request, "report_error.html", {'user_prof': user_prof, 'contrib_prof': contrib_prof})
            else:
                return render(request, "home.html", {'user_prof': user_prof})
        else:
            return render(request, "home.html")



