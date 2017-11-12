from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.urls import reverse
from ...profiles.models.user_models import UserProfile
from ...profiles.models.contributor_model import ContributorProfile
from ..models.content_creation_model import ContentCreation
from django.urls import reverse_lazy
from itertools import chain
from ..forms.content_creation_form import ContentCreateForm, CkEditorForm
from django.contrib import messages
from datetime import datetime
from PIL import Image
from django.conf import settings
from ..modules.post_util import display_error
from ...profiles.modules.contributor_util import user_can_contribute
from django.core.exceptions import ObjectDoesNotExist
from braces.views import LoginRequiredMixin
from django.views.generic import DeleteView
from django.core.exceptions import PermissionDenied
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
import os.path
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

from django.views import generic


class ContentCreationView(View):
    '''
    View for the main Content Creation page. Lists all Content Creation posts. Returns a regular user to the
    home page since it is not directed towards them, allows contributors access, and allows the user "relevate@outlook.com"
    to edit, delete, and create posts.
    '''
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            user_prof = UserProfile.objects.get(user=user)
            if user_prof.is_contributor:
                contrib_prof = ContributorProfile.objects.get(user_profile=user_prof)
                can_edit = False
                posts = ContentCreation.objects.all()
                # checks the group "Content Creation Contributor" for the user. If this group has not yet been created, create
                # and assign users in the admin page.
                public_scholarship_or_content_creation = "content_creation"
                if user.groups.filter(name='Content Creation Contributor').exists():
                    can_edit = True
                return render(request, "content_creation.html",
                              {'user_prof': user_prof, 'contrib_prof': contrib_prof, 'can_edit': can_edit, 'posts': posts})
            else:
                return render(request, "home.html", {'user_prof': user_prof})
        else:
            return render(request, "home.html")


class ContentCreationCreateView(LoginRequiredMixin, View):
    '''
    View for creating a new Content Creation Post, only relevate@outlook.com or user in permissions group will return
    content_creation_create.html
    '''
    def get(self, request, slug):
        if request.user.is_authenticated:
            user = request.user
            user_prof = UserProfile.objects.get(user=user)
            form = ContentCreateForm
            contrib_prof = ContributorProfile.objects.get(user_profile=user_prof)
            #if the user has clicked on the "new post" button from the content creation page
            if slug == 'content_creation':
                # variable used in template to show level and type for content creation
                public_scholarship_or_content_creation = False
                form = ContentCreateForm(initial={'public_scholarship_or_content_creation': False})



            #if the user has clicked on the "new post" button from the public scholarship page
            else:
                #variable used in template to hide level and type for public scholarship
                public_scholarship_or_content_creation = True
                data = {'type': 'Infographics', 'level': 'Expanding Your Reach', 'public_scholarship_or_content_creation': True}
                form = ContentCreateForm(initial=data)


                #checks the group "Content Creation Contributor" for the user. If this group has not yet been created, create
                # and assign users in the admin page.
            if user.groups.filter(name='Content Creation Contributor').exists():
                return render(request, "content_creation_create.html",
                              {'user_prof': user_prof, 'contrib_prof': contrib_prof, 'form': form, 'public_scholarship_or_content_creation': public_scholarship_or_content_creation})
            else:
                return render(request, "home.html", {'user_prof': user_prof})
        else:
            return render(request, "home.html")

    def post(self, request, *args, **kwargs):

        user = request.user
        user_prof = UserProfile.objects.get(user=user)
        contrib_prof = ContributorProfile.objects.get(user_profile=user_prof)
        form = ContentCreateForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data.get('content')
            alternate_content = form.cleaned_data.get('alternate_content')
            x = form.cleaned_data.get('x')
            y = form.cleaned_data.get('y')
            w = form.cleaned_data.get('width')
            h = form.cleaned_data.get('height')
            image = form.cleaned_data.get('image')
            content_file = form.cleaned_data.get('content_file')
            blurb = form.cleaned_data.get('blurb')
            references = form.cleaned_data.get('references')
            type = form.cleaned_data.get('type')
            level = form.cleaned_data.get('level')
            public_scholarship_or_content_creation = form.cleaned_data.get('public_scholarship_or_content_creation')
            contributor_profile = ContributorProfile.objects.get(user_profile=user_prof)
            if user.groups.filter(name='Content Creation Contributor').exists():
                contributor_profile = user_can_contribute(request.user)
                new_content_creation = ContentCreation(
                    contributor=contributor_profile,
                    title=title,
                    image=image,
                    blurb=blurb,
                    references=references,
                    type=type,
                    level=level,
                    publishedDate=datetime.utcnow(),
                    public_scholarship_or_content_creation=public_scholarship_or_content_creation
                )
                new_content_creation.save()
                if content:
                    new_content_creation.content = content
                if content_file:
                    new_content_creation.content_file = content_file
                # If user inputs image file instead of url
                if image:
                    # Gets the original image to be cropped
                    photo = Image.open(form.cleaned_data.get('image'))
                    # Cropps the image using values x,y,w,and h from the form
                    cropped_image = photo.crop((x, y, w + x, h + y))
                    # Splits the file name and the extension
                    filename, file_extension = os.path.splitext(
                        os.path.basename(urlparse(new_content_creation.image.url).path))
                    cropped_image.save(settings.BASE_DIR + "/media/content_creation/images/" + filename + file_extension)
                    new_content_creation.image = "content_creation/images/" + filename + file_extension
                new_content_creation.save()

                messages.success(request, "Content Creation Post Was Successfully Created!")

                print ("Article went through")
                if public_scholarship_or_content_creation == True:
                    return HttpResponseRedirect(reverse_lazy('contribution:public_scholarship'))
                else:
                    return HttpResponseRedirect(reverse_lazy('contribution:content_creation'))
            else:
                return HttpResponseRedirect(reverse_lazy("contribution:home"))
        else:
            print("Invalid")
            display_error(form, request)
            return render(request, 'content_creation_create.html',
                          {
                              'form': form,
                              'user_prof': user_prof,
                              'first_name': request.user.first_name,
                              'last_name': request.user.last_name
                          })

class ContentCreationIndividualView(LoginRequiredMixin, View):
    """
        Class for view individual posts
    """

    def get(self, request, slug):
        """
        The get request for the view

        :param slug: this is a unique url identifier for each post

        """
        user_prof = UserProfile.objects.get(user=request.user)
        try:
            post = ContentCreation.objects.get(slug=str(slug))
            contributor = user_can_contribute(request.user)
            is_user_article = False
            if user_prof.is_contributor == True:
                #only the relevate account or the person who created the post should be able to edit their own post.
                if contributor.id is post.contributor.id or user_prof.user.email == "relevate@outlook.com":
                    is_user_article = True
            else:
                post.views = post.views + 1
                post.save()
            content_file_extension = None
            if post.content_file:
                name, content_file_extension = os.path.splitext(post.content_file.name)
                content_file_extension = content_file_extension[1:]
                print( content_file_extension)
            return render(request, 'content_create_view.html',
                {
                    'is_user_article':is_user_article,
                    'user_prof':user_prof,
                    'post': post,
                    'first_name':request.user.first_name,
                    'last_name':request.user.last_name,
                    'content_file_extension': content_file_extension
                })
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('contribution:content_creation'))

class ContentCreationUpdateView(LoginRequiredMixin, View):

    def get(self, request, slug):

        user_prof = UserProfile.objects.get(user=request.user)
        try:
            post = ContentCreation.objects.get(slug=str(slug))

            form = ContentCreateForm(
                initial={
                    'title': post.title,
                    'content': post.content,
                    'isPublished': post.isPublished,
                    'image': post.image,
                    'blurb': post.blurb,
                    'references': post.references,
                    'content_file': post.content_file,
                    'type': post.type,
                    'level': post.level,
                })
            return render(request, 'content_creation_update.html',
                          {
                              'form': form,
                              'user_prof': user_prof,
                              'post': post,
                          })
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('contribution:content_creation'))

    def post(self, request, slug):

        user_prof = UserProfile.objects.get(user=request.user)
        contrib_prof = ContributorProfile.objects.get(user_profile=user_prof)
        content_creation = ContentCreation.objects.get(slug=slug)
        form = ContentCreateForm(request.POST, request.FILES)
        if form.is_valid():
            content_creation.title = form.cleaned_data.get("title")
            content_creation.content = form.cleaned_data.get("content")
            content_creation.references = form.cleaned_data.get('references')
            image = form.cleaned_data.get("image")
            content_creation.blurb = form.cleaned_data.get('blurb')
            content_creation.content_file = form.cleaned_data.get('content_file')
            content_creation.type = form.cleaned_data.get('type')
            content_creation.level = form.cleaned_data.get('level')

            x = form.cleaned_data.get('x')
            y = form.cleaned_data.get('y')
            w = form.cleaned_data.get('width')
            h = form.cleaned_data.get('height')

            # If user inputs image file instead of url
            if image:
                content_creation.image = image
                # Gets the original image to be cropped
                photo = Image.open(image)
                # Crops the image using values x,y,w,and h from the form
                cropped_image = photo.crop((x, y, w + x, h + y))
                # Splits the file name and the extension
                filename, file_extension = os.path.splitext(os.path.basename(urlparse(image.name).path))
                cropped_image.save(settings.BASE_DIR + "/media/content_creation/images/" + filename + file_extension)
                content_creation.image = "content_creation/images/" + filename + file_extension
            content_creation.save()
            content_creation.updateDate = datetime.utcnow()

            if (request.POST.get('hidden-publish-checkbox') == "on"):
                content_creation.publishDate = datetime.utcnow()
                content_creation.isPublished = True
                messages.success(request, "Post Was Successfully Published!")
            else:

                messages.success(request, "Post Was Successfully Updated!")
                content_creation.save()

            return HttpResponseRedirect(reverse_lazy("contribution:content_creation_views", kwargs={'slug': slug}))
        display_error(form, request)
        return render(request, 'content_creation_update.html',
                      {
                          'form': form,
                          'user_prof': user_prof,
                          'post': content_creation,
                          'first_name': request.user.first_name,
                          'last_name': request.user.last_name
                      })

class PermissionMixin(object):

    def get_object(self, *args, **kwargs):
        obj = super(PermissionMixin, self).get_object(*args, **kwargs)
        #allow the obj to be returned if the user is logged in as relevate
        if self.request.user.email == 'relevate@outlook.com':
            return obj
        if not obj.contributor.user_profile.user == self.request.user:
            raise PermissionDenied()
        #allow the obj to be returned if user is the owner of the post.
        else:
            return obj

class ContentCreationRemoveView(PermissionMixin, DeleteView):
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

    model = ContentCreation
    success_url = reverse_lazy('contribution:content_creation')













class CkEditorFormView(generic.FormView):
    form_class = ContentCreateForm
    template_name = 'form.html'

    def get_success_url(self):
        return reverse('ckeditor-form')


ckeditor_form_view = CkEditorFormView.as_view()