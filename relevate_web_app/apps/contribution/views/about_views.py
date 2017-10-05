from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import View, FormView
from ...profiles.models.user_models import UserProfile
from ...profiles.models.contributor_model import ContributorProfile
from ..models.about_person_model import AboutPerson
from ..forms.about_forms import AboutFunderForm
from django.conf import settings
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
import os.path
from ..modules.post_util import display_error
from braces.views import LoginRequiredMixin
from django.views.generic import DeleteView
from PIL import Image
from django.core.exceptions import PermissionDenied

class AboutView(View):

    '''
    Relevate About View
    '''

    def get(self, request):
        """
        Displays the about page containing the team members and
        contact info
        """
        about_persons = AboutPerson.objects.all()
        funders = about_persons.filter(funder_or_adviser='funder').order_by('position')
        advisers = about_persons.filter(funder_or_adviser='adviser').order_by('position')
        architects = about_persons.filter(funder_or_adviser='architect').order_by('position')
        engineers = about_persons.filter(funder_or_adviser='engineer').order_by('position')
        previous_architects = about_persons.filter(funder_or_adviser='previous architect').order_by('position')
        previous_engineers = about_persons.filter(funder_or_adviser='previous engineer').order_by('position')
        can_edit = False
        if request.user.is_authenticated:
            user_prof = UserProfile.objects.get(user=request.user)
            if user_prof.user.email == "relevate@outlook.com":
                can_edit = True
            if (user_prof.is_contributor):
                contrib_prof = ContributorProfile.objects.get(user_profile=user_prof)
                return render(request, "about.html", {'user_prof': user_prof, 'contrib_prof': contrib_prof, 'funders': funders,
                  'advisers': advisers, 'architects': architects, 'engineers': engineers,
                  'previous_architects': previous_architects, 'previous_engineers': previous_engineers,'can_edit': can_edit})
            else:
                return render(request, "about.html", {'user_prof': user_prof, 'funders': funders, 'advisers': advisers,
                'architects': architects, 'engineers': engineers, 'previous_architects': previous_architects,
                'previous_engineers': previous_engineers,'can_edit': can_edit})
        else:
            return render(request, "about.html", {'funders': funders, 'advisers': advisers, 'architects': architects,
            'engineers': engineers, 'previous_architects': previous_architects, 'previous_engineers': previous_engineers, 'can_edit': can_edit})


class AboutCreateView(LoginRequiredMixin, FormView):
    """
        A class that represents the a new about creation page.
    """

    def get(self, request, *args, **kwargs):
        """

        The get request to view the page to create a new entry on the about page

        :return: an http response showing the article form for creating new entry on the about page

        """
        user_prof = UserProfile.objects.get(user=request.user)
        form = AboutFunderForm()
        #ATTENTION! change email if you ever want to allow more users to be able to edit funders or contributors.
        if not user_prof.user.email == "relevate@outlook.com":
            return HttpResponseRedirect(reverse("contribution:home"))
        return render(request, 'about_create.html',
                      {
                          'form': form,
                          'user_prof': user_prof,
                          'first_name': request.user.first_name,
                          'last_name': request.user.last_name
                      })

    def post(self, request, *args, **kwargs):
        """
            The post request for creating a new entry on the about page

            :return: an http response that redirects to a new page if about creation is successful
        """
        user_prof = UserProfile.objects.get(user=request.user)
        form = AboutFunderForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            content = form.cleaned_data.get('content')
            funder_or_adviser = form.cleaned_data.get('funder_or_adviser')
            x = form.cleaned_data.get('x')
            y = form.cleaned_data.get('y')
            w = form.cleaned_data.get('width')
            h = form.cleaned_data.get('height')
            image = form.cleaned_data.get('image')
            # ATTENTION! change email if you ever want to allow more users to be able to edit funders or contributors.
            if user_prof.user.email == "relevate@outlook.com":
                new_about_person = AboutPerson(
                    name=name,
                    content=content,
                    image=image,
                    funder_or_adviser=funder_or_adviser
                )
                new_about_person.save()
                # If user inputs image file instead of url
                if image:
                    # Gets the original image to be cropped
                    photo = Image.open(form.cleaned_data.get('image'))
                    # Cropps the image using values x,y,w,and h from the form
                    cropped_image = photo.crop((x, y, w + x, h + y))
                    # Splits the file name and the extension
                    filename, file_extension = os.path.splitext(
                        os.path.basename(urlparse(new_about_person.image.url).path))
                    cropped_image.save(settings.BASE_DIR + "/media/about_person/image/" + filename + file_extension)
                    print(filename)
                    print(file_extension)
                    print(settings.BASE_DIR + "/media/about_person/image/" + filename + file_extension)
                    new_about_person.image = "about_person/image/" + filename + file_extension
                    print(new_about_person.image)
                new_about_person.save()
                messages.success(request, "Funder or Advisor Was Successfully Added!")
                return HttpResponseRedirect(reverse_lazy('contribution:about'))
            else:
                return HttpResponseRedirect(reverse_lazy("contribution:home"))
        else:
            print("Invalid")
            display_error(form, request)
            return render(request, 'about_create.html',
                          {
                              'form': form,
                              'user_prof': user_prof,
                          })

class AboutUpdateView(LoginRequiredMixin, View):
    """
        A class that represents the update page for an about page entry
    """

    def get(self, request, slug):
        """

        The get request to view the update page for an entry on the about page

        :return: an http response showing the aboutPerson form for creating new about entry

        """
        user_prof = UserProfile.objects.get(user=request.user)
        try:
            about_person = AboutPerson.objects.get(slug=str(slug))
            form = AboutFunderForm(
            initial={
                'name': about_person.name,
                'content': about_person.content,
                'image': about_person.image,
                'funder_or_adviser': about_person.funder_or_adviser
            })
            user_prof = UserProfile.objects.get(user=request.user)
            # ATTENTION! change email if you ever want to allow more users to be able to edit funders or contributors.
            if not user_prof.user.email == "relevate@outlook.com":
                return HttpResponseRedirect(reverse("contribution:home"))
            return render(request, 'about_update.html',
                          {
                              'form': form,
                              'slug': slug,
                              'user_prof': user_prof,
                              'first_name': request.user.first_name,
                              'last_name': request.user.last_name
                          })
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('contribution:about'))


    def post(self, request, slug):
        """
            The post request for updating an existing entry on the about page.

            :return: an http response that redirects to a new page if the entry update is successful
        """
        user_prof = UserProfile.objects.get(user=request.user)
        about_person = AboutPerson.objects.get(slug=slug)
        form = AboutFunderForm(request.POST, request.FILES)
        if form.is_valid():
            x = form.cleaned_data.get('x')
            y = form.cleaned_data.get('y')
            w = form.cleaned_data.get('width')
            h = form.cleaned_data.get('height')
            image = form.cleaned_data.get('image')
            # ATTENTION! change email if you ever want to allow more users to be able to edit funders or contributors.
            if user_prof.user.email == "relevate@outlook.com":
                about_person.name = form.cleaned_data['name']
                about_person.content = form.cleaned_data.get('content')
                about_person.funder_or_adviser = form.cleaned_data.get('funder_or_adviser')
                # If user inputs image file instead of url
                if image:
                    # Gets the original image to be cropped
                    photo = Image.open(form.cleaned_data.get('image'))
                    # Cropps the image using values x,y,w,and h from the form
                    cropped_image = photo.crop((x, y, w + x, h + y))
                    # Splits the file name and the extension
                    filename, file_extension = os.path.splitext(
                        os.path.basename(urlparse(about_person.image.url).path))
                    cropped_image.save(settings.BASE_DIR + "/media/about_person/image/" + filename + file_extension)
                    about_person.image = "about_person/image/" + filename + file_extension
                about_person.save()
                messages.success(request, "Funder or Advisor Was Successfully Added!")
                return HttpResponseRedirect(reverse_lazy('contribution:about'))
            else:
                return HttpResponseRedirect(reverse_lazy("contribution:home"))
        else:
            print("Invalid")
            display_error(form, request)
            return render(request, 'about_create.html',
                          {
                              'form': form,
                              'user_prof': user_prof,
                          })

class PermissionMixin(object):

    '''
    permission mixin to check user's permissions
    '''

    def get_object(self, *args, **kwargs):
        obj = super(PermissionMixin, self).get_object(*args, **kwargs)
        if self.request.user.email == 'relevate@outlook.com':
            return obj
        if not obj.contributor.user_profile.user == self.request.user:
            raise PermissionDenied()
        else:
            return obj

class AboutRemoveView(PermissionMixin, DeleteView):

    '''
    A DeleteView for the AboutPerson model. Will delete an AboutPerson object when it is given.
    '''

    model = AboutPerson
    success_url = reverse_lazy('contribution:about')